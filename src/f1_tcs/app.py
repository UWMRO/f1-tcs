#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: app.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from typing import AsyncIterator

from fastapi import FastAPI


logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for FastAPI app."""

    yield  # Do nothing for now.


app = FastAPI(swagger_ui_parameters={"tagsSorter": "alpha"}, lifespan=lifespan)


@app.get("/")
def root():
    return {}


@app.get("/test")
def test():
    return {"result": True}
