#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: ascom.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
import re

from typing import Literal

import httpx

from f1_tcs import config


class ASCOMError(Exception):
    """Exception raised for ASCOM errors."""

    def __init__(self, code: int, message: str, path: str = ""):
        self.error_message = message
        self.code = 0
        self.path = path

        super().__init__(
            f"ASCOM error on path {self.path}: {self.code}: {self.error_message}"
        )


class ASCOM:
    """Communication with the ASCOM server."""

    def __init__(self, host: str, port: int, device: int = 0):
        self.host = host
        self.port = port
        self.device = device

    async def __call__(
        self,
        path: str,
        method: Literal["GET", "PUT"] = "GET",
        raise_on_error: bool = True,
        **params,
    ) -> dict:
        """Call the ASCOM server with the given path and method."""

        return await self.call_telescope_path(
            path,
            method=method,
            raise_on_error=raise_on_error,
            **params,
        )

    async def call_telescope_path(
        self,
        path: str,
        method: Literal["GET", "PUT"] = "GET",
        raise_on_error: bool = True,
        **params,
    ) -> dict:
        """Call the ASCOM telescope path with parameters.

        Parameters
        ----------
        path
            The path to call. The path does not need to include the
            ``/telescope/<device>`` prefix.
        method
            The HTTP method to use. Either ``GET`` or ``PUT``.
        raise_on_error
            If ``True``, raise an exception on error. This only affects ASCOM
            error messages. Any non-200 HTTP status codes will raise an exception.
        params
            The search parameters to pass to the ASCOM server. This is a dictionary
            of key-value pairs.

        Returns
        -------
        dict
            The response from the ASCOM server.

        """

        # Base URL for the ASCOM server.
        api_version = config["ascom"]["api_version"]
        base_url = f"http://{self.host}:{self.port}/api/{api_version}/"

        # If the path does not include the telescope prefix, add it.
        tel_prefix = f"telescope/{self.device}"
        if tel_prefix not in path:
            path = f"{tel_prefix}/{path}"

        # Normalise the path.
        path = re.sub(r"/{2,}", "/", path)

        # Query the ASCOM server.
        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.request(
                method,
                path,
                params=params,
                timeout=config["ascom"]["timeout"],
            )
            response.raise_for_status()

        data = response.json()
        if "ErrorNumber" in data:
            if raise_on_error and data["ErrorNumber"] != 0:
                raise ASCOMError(
                    message=data["ErrorMessage"],
                    code=data["ErrorNumber"],
                    path=path,
                )

        return {
            "result": data["Value"],
            "error_number": data["ErrorNumber"],
            "error_message": data["ErrorMessage"] or None,
        }

    async def gather(
        self,
        *paths: str,
        method: Literal["GET", "PUT"] = "GET",
        raise_on_error: bool = True,
        **params,
    ) -> dict[str, dict]:
        """Gather multiple ASCOM calls into a single request."""

        if isinstance(paths[0], (list, tuple)):
            paths = paths[0]  # type: ignore

        # Gather the paths into a single request.
        tasks = [
            self.call_telescope_path(path, method, raise_on_error, **params)
            for path in paths
        ]

        # Run the tasks and return the results.
        results = await asyncio.gather(*tasks)

        return {
            path: {
                "result": results[ipath]["result"],
                "error_number": results[ipath]["error_number"],
                "error_message": results[ipath]["error_message"],
            }
            for ipath, path in enumerate(paths)
        }

    async def test(self) -> bool:
        """Test the ASCOM connection."""

        try:
            await self.call_telescope_path(
                "connected",
                method="GET",
                raise_on_error=True,
            )
        except Exception:
            return False
        else:
            return True


ascom = ASCOM(
    config["ascom"]["host"],
    config["ascom"]["port"],
    device=config["ascom"]["device"],
)


def with_ascom() -> ASCOM:
    """Dependency to get the ASCOM instance."""

    return ascom
