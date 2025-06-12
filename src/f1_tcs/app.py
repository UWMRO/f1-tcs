#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: app.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from contextlib import asynccontextmanager

from typing import Annotated, AsyncIterator

from fastapi import Depends, FastAPI

from f1_tcs.ascom import ASCOM
from f1_tcs.dependencies import ascom
from f1_tcs.routers.ascii import router as ascii_router
from f1_tcs.routers.status import router as status_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for FastAPI app."""

    yield  # Do nothing for now.


app = FastAPI(swagger_ui_parameters={"tagsSorter": "alpha"}, lifespan=lifespan)
app.include_router(status_router)
app.include_router(ascii_router)


@app.get("/")
def root():
    return {}


@app.get("/test/ping")
def ping():
    """Confirm the API is running."""

    return {"result": True}


@app.get("/test/ascom")
async def test(ascom: Annotated[ASCOM, Depends(ascom)]):
    """Test the ASCOM connection."""

    return await ascom.test()
