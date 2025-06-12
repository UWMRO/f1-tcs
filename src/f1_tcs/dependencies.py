#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2025-05-12
# @Filename: dependencies.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from f1_tcs.ascii import F1_ASCII_Server
from f1_tcs.ascom import ASCOM


__all__ = ["ascom"]


def ascom() -> ASCOM:
    """Dependency to get the ASCOM instance."""

    return ASCOM.from_config()


async def ascii() -> F1_ASCII_Server:
    """Dependency to get the F1_ASCII_Server instance."""

    ascii_client = F1_ASCII_Server.from_config()
    await ascii_client.connect()

    return ascii_client
