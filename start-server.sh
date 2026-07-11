#!/bin/bash

source .venv/bin/activate
uvicorn f1_tcs.app:app --port 9090 --workers 1 --log-level debug
