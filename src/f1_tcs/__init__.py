#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import pathlib

from yaml import safe_load


CONFIG = pathlib.Path(__file__).parent / "config.yaml"


def load_config() -> dict:
    """Load the configuration file."""

    with open(CONFIG, "r") as f:
        config = safe_load(f)

    return config


config = load_config()


__all__ = ["config"]
