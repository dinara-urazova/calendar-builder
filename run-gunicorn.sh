#!/usr/bin/env sh

# source .venv/bin/activate
gunicorn -w 4 -b 0.0.0.0 calendar_builder:app
# deactivate

