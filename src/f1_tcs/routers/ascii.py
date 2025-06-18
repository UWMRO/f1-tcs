#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2025-06-12
# @Filename: ascii.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio

from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from f1_tcs.dependencies import ascii
from f1_tcs.protocols.ascii import ASCIIError
from f1_tcs.tools import parse_scope_status


if TYPE_CHECKING:
    from f1_tcs.protocols.ascii import ASCII_Protocol


router = APIRouter(prefix="/ascii", tags=["ascii"])


class StatusResponse(BaseModel):
    """Response model for the status endpoint."""

    bool_params: Annotated[
        int,
        Field(description="Bitmask indicating the status of the telescope."),
    ]
    bool_params_labels: Annotated[
        list[str],
        Field(description="Labels for the boolean parameters in the status bitmask."),
    ]
    right_ascension: Annotated[
        float,
        Field(description="Right ascension of the telescope."),
    ]
    declination: Annotated[
        float,
        Field(description="Declination of the telescope."),
    ]
    altitude: Annotated[
        float,
        Field(description="Altitude of the telescope."),
    ]
    azimuth: Annotated[
        float,
        Field(description="Azimuth of the telescope."),
    ]
    secondary_axis_angle: Annotated[
        float,
        Field(description="Secondary axis angle of the telescope."),
    ]
    primary_axis_angle: Annotated[
        float,
        Field(description="Primary axis angle of the telescope."),
    ]
    scope_sidereal_time: Annotated[
        float,
        Field(description="Scope sidereal time."),
    ]
    scope_julian_day: Annotated[
        float,
        Field(description="Scope Julian day."),
    ]
    scope_time: Annotated[
        float,
        Field(description="Scope time."),
    ]
    air_mass: Annotated[
        float,
        Field(description="Airmass."),
    ]


@router.get(
    "/status", response_model=StatusResponse, summary="Get the status of the telescope"
)
async def status(ascii: ASCII_Protocol = Depends(ascii)):
    """Get the status of the telescope."""

    try:
        status = await ascii.send_command("ReadScopeStatus")
        parsed_status = parse_scope_status(status)
        return StatusResponse(**parsed_status)

    except ASCIIError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get(
    "/sync_to_zenith",
    response_model=bool,
    summary="Sync the telescope to zenith",
)
async def sync_to_zenith(ascii: ASCII_Protocol = Depends(ascii)):
    """Sets the Zenith as the current pointing position of the telescope."""

    try:
        await ascii.send_command("UnPark")
        await ascii.send_command("SyncToAltAz 0 89.9")
        await ascii.send_command("MotorsToAuto")

        await asyncio.sleep(3)

        await ascii.send_command("Park")
    except ASCIIError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return True


@router.get("/park", response_model=bool, summary="Park the telescope")
async def park(ascii: ASCII_Protocol = Depends(ascii)):
    """Parks the telescope at Zenith."""

    try:
        await ascii.send_command("Park")
    except ASCIIError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return True


@router.get("/goto_cover", response_model=bool, summary="Goto cover position")
async def goto_cover(ascii: ASCII_Protocol = Depends(ascii)):
    """Goes to the cover position."""

    try:
        await ascii.send_command("UnPark")
        await ascii.send_command("GoToAltAzStop 180 20")

        await asyncio.sleep(70)
        await ascii.send_command("Abort")
    except ASCIIError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return True


@router.get("/stop", response_model=bool, summary="Stops the telescope")
async def stop(ascii: ASCII_Protocol = Depends(ascii)):
    """Stops the telescope."""

    try:
        await ascii.send_command("Abort")
    except ASCIIError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return True
