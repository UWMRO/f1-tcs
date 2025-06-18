#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: ascom.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from f1_tcs.dependencies import ascom


if TYPE_CHECKING:
    from f1_tcs.protocols.ascom import ASCOM_Protocol


router = APIRouter(prefix="/ascom", tags=["ascom"])


class ASCOMStatusResponse(BaseModel):
    """Response model for the ASCOM status endpoint."""

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
        float | None,
        Field(description="Declination of the telescope"),
    ]

    errors: Annotated[
        list[str],
        Field(description="List of parameters with errors"),
    ]


@router.get("/test")
async def test(ascom: Annotated[ASCOM_Protocol, Depends(ascom)]):
    """Test the ASCOM connection."""

    return await ascom.test()


@router.get("/pointing", response_model=ASCOMStatusResponse)
async def status(ascom: Annotated[ASCOM_Protocol, Depends(ascom)]):
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

    return ASCOMStatusResponse(
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
