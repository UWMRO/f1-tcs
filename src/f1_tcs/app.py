#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: app.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from typing import Annotated, AsyncIterator

from fastapi import Depends, FastAPI

from f1_tcs.ascom import ASCOM, with_ascom
from f1_tcs.routers.status import router as status_router


logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for FastAPI app."""

    yield  # Do nothing for now.


app = FastAPI(swagger_ui_parameters={"tagsSorter": "alpha"}, lifespan=lifespan)
app.include_router(status_router)


@app.get("/")
def root():
    return {}


@app.get("/test/ping")
def ping():
    """Confirm the API is running."""

    return {"result": True}


@app.get("/test/ascom")
async def test(ascom: Annotated[ASCOM, Depends(with_ascom)]):
    """Test the ASCOM connection."""

    return await ascom.test()
