#!/usr/bin/env bash

source .venv/bin/activate
gunicorn -w 4 calendar-builder:app
deactivate
