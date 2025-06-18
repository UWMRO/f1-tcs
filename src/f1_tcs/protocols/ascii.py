#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2025-06-12
# @Filename: ascii.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
import os

from f1_tcs import config, logger


class ASCIIError(Exception):
    """Exception raised for errors in the ASCII protocol."""

    pass


class ASCII_Protocol:
    """A class to connect to the F1 ASCII server."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None

    @classmethod
    def from_config(cls) -> ASCII_Protocol:
        """Create an ``ASCII_Protocol`` instance from the configuration file."""

        simulator = os.getenv("F1_TCS_SIMULATOR", "false").lower()
        if simulator in ("true", "1", "yes"):
            host = config["f1_ascii"]["simulator"]["host"]
            port = config["f1_ascii"]["simulator"]["port"]
        else:
            host = config["f1_ascii"]["host"]
            port = config["f1_ascii"]["port"]

        return cls(host=host, port=port)

    async def connect(self):
        """Connect to the F1 ASCII server."""

        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        logger.debug(f"Connected to ASCII server at {self.host}:{self.port}")

    async def disconnect(self):
        """Disconnect from the F1 ASCII server."""

        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            logger.debug(f"Disconnected from ASCII server at {self.host}:{self.port}")

    async def send_command(self, command: str) -> str:
        """Send a command to the F1 ASCII server and return the response.

        TODO: parse the response and confirm if the command was successful. This
        is a bit hard to do at a general level because the command reponses are not
        standardized.

        """

        # Just to be sure.
        await self.disconnect()

        # Connect to the server.
        await self.connect()
        assert self.writer and self.reader, "Connection to ASCII server failed."

        # Send the command.
        if not command.endswith("\n"):
            command += "\n"

        try:
            self.writer.write(command.encode())
            await self.writer.drain()

            # Wait for a response.
            response = await asyncio.wait_for(self.reader.readline(), timeout=1.0)
            return response.decode().strip()

        except asyncio.TimeoutError:
            logger.error(f"Timeout while waiting for response to command: {command}")
            raise ASCIIError(f"Timed out waiting for response to command: {command}")

        except Exception as e:
            logger.error(f"Error sending command '{command}': {e}")
            raise ASCIIError(f"Error sending command '{command}': {e}")

        finally:
            # Ensure we disconnect after sending the command.
            await self.disconnect()
