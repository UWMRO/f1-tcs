#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2025-05-12
# @Filename: dependencies.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from f1_tcs.protocols.ascii import ASCII_Protocol
from f1_tcs.protocols.ascom import ASCOM_Protocol


__all__ = ["ascom", "ascii"]


def ascom() -> ASCOM_Protocol:
    """Dependency to get the ASCOM instance."""

    return ASCOM_Protocol.from_config()


async def ascii() -> ASCII_Protocol:
    """Dependency to get the ``ASCII_Protocol`` instance."""

    return ASCII_Protocol.from_config()
