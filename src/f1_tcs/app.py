#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: app.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from contextlib import asynccontextmanager

from typing import AsyncIterator

from fastapi import FastAPI

from f1_tcs import logger
from f1_tcs.protocols import ASCII_Protocol, ASCOM_Protocol
from f1_tcs.routers.ascii import router as ascii_router
from f1_tcs.routers.ascom import router as status_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for FastAPI app."""

    try:
        ascii_instance = ASCII_Protocol.from_config()
        app.state.ascii_instance = ascii_instance
    except Exception as e:
        logger.error(f"Failed to create ASCII_Protocol instance: {e}")
        app.state.ascii_instance = None

    try:
        ascom_instance = ASCOM_Protocol.from_config()
        app.state.ascom_instance = ascom_instance
    except Exception as e:
        logger.error(f"Failed to create ASCOM_Protocol instance: {e}")
        app.state.ascom_instance = None

    yield  # Do nothing for now.


app = FastAPI(swagger_ui_parameters={"tagsSorter": "alpha"}, lifespan=lifespan)
app.include_router(status_router)
app.include_router(ascii_router)


@app.get("/")
def root():
    return {}


@app.get("/ping")
def ping():
    """Confirm the API is running."""

    return {"result": True}
