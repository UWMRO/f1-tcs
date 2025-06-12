#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2025-06-12
# @Filename: ascii.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio

from f1_tcs import config, logger


class F1_ASCII_Server:
    """A class to connect to the F1 ASCII server."""

    def __init__(self, host: str, port: int, device: int = 0):
        self.host = host
        self.port = port

        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None

    @classmethod
    def from_config(cls) -> F1_ASCII_Server:
        """Create an F1_ASCII_Server instance from the configuration file."""

        ascii_config = config["f1_ascii"]
        return cls(
            host=ascii_config["host"],
            port=ascii_config["port"],
        )

    async def connect(self):
        """Connect to the F1 ASCII server."""

        self.reader, self.writer = await asyncio.open_connection(
            self.host,
            self.port,
        )
        logger.info(f"Connected to F1 ASCII server at {self.host}:{self.port}")

    async def disconnect(self):
        """Disconnect from the F1 ASCII server."""

        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            logger.info(f"Disconnected from F1 ASCII server at {self.host}:{self.port}")

    async def send_command(self, command: str) -> bool:
        """Send a command to the F1 ASCII server and return the response.

        TODO: parse the response and confirm if the command was successful. This
        is a bit hard to do at a general level because the command reponses are not
        standardized.

        """

        if not self.writer or self.writer.is_closing():
            logger.warning("Not connected to the F1 ASCII server. Reconnecting...")
            await self.disconnect()
            await self.connect()

            if not self.writer or self.writer.is_closing():
                raise RuntimeError("Not connected to the F1 ASCII server.")

        if not command.endswith("\n"):
            command += "\n"

        self.writer.write(command.encode())
        await self.writer.drain()

        print(await self.reader.readline())

        await self.disconnect()

        return True
