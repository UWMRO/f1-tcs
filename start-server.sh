#!/bin/bash

source .venv/bin/activate
fastapi run src/f1_tcs/app.py --port 9090 --workers 1
