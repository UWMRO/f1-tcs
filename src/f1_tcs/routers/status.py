#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from f1_tcs.ascom import ASCOM, with_ascom


router = APIRouter(
    prefix="/status",
    tags=["status"],
)


class StatusResponse(BaseModel):
    """Response model for the status endpoint."""

    utcdate: Annotated[
        str | None,
        Field(description="UTC date and time"),
    ]
    sidereal_time: Annotated[
        float | None,
        Field(description="Sidereal time"),
    ]
    ha: Annotated[
        float | None,
        Field(description="Hour angle"),
    ]
    altitude: Annotated[
        float | None,
        Field(description="Altitude of the telescope"),
    ]
    azimuth: Annotated[
        float | None,
        Field(description="Azimuth of the telescope"),
    ]
    right_ascension: Annotated[
        float | None,
        Field(description="Right ascension of the telescope"),
    ]
    declination: Annotated[
        float | None, Field(description="Declination of the telescope")
    ]

    errors: Annotated[
        list[str],
        Field(description="List of parameters with errors"),
    ]


@router.get("/pointing", response_model=StatusResponse)
async def status(ascom: Annotated[ASCOM, Depends(with_ascom)]):
    """Get the status of the telescope."""

    try:
        data = await ascom.gather(
            "utcdate",
            "siderealtime",
            "altitude",
            "azimuth",
            "rightascension",
            "declination",
            raise_on_error=False,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting status: {e}",
        )

    ha: float | None = None
    if (
        data["siderealtime"]["error_number"] == 0
        and data["rightascension"]["error_number"] == 0
    ):
        ha = data["siderealtime"]["result"] - data["rightascension"]["result"]

    return StatusResponse(
        utcdate=data["utcdate"]["result"],
        sidereal_time=data["siderealtime"]["result"],
        ha=ha,
        altitude=data["altitude"]["result"],
        azimuth=data["azimuth"]["result"],
        right_ascension=data["rightascension"]["result"] * 15
        if data["rightascension"]["result"] is not None
        else None,
        declination=data["declination"]["result"],
        errors=[key for key, value in data.items() if value["error_number"] != 0],
    )
