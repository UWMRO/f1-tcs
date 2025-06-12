#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2025-06-12
# @Filename: ascii.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from fastapi import APIRouter, Depends

from f1_tcs.ascii import F1_ASCII_Server
from f1_tcs.dependencies import ascii


router = APIRouter(prefix="/ascii", tags=["ascii"])


@router.get(
    "/sync_to_zenith",
    response_model=bool,
    summary="Sync the telescope to zenith",
)
async def sync_to_zenith(ascii: F1_ASCII_Server = Depends(ascii)):
    """Sets the Zenith as the current pointing position of the telescope."""

    await ascii.send_command("UnPark")
    await ascii.send_command("SyncToAltAz 180 89.9")

    return True


@router.get("/park", response_model=bool, summary="Park the telescope")
async def park(ascii: F1_ASCII_Server = Depends(ascii)):
    """Parks the telescope at Zenith."""

    await ascii.send_command("Park")

    return True


@router.get("/goto_cover", response_model=bool, summary="Goto cover position")
async def goto_cover(ascii: F1_ASCII_Server = Depends(ascii)):
    """Goes to the cover position."""

    await ascii.send_command("UnPark")
    await ascii.send_command("GoToAltAz 180 70")

    return True
