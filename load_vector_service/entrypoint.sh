#!/bin/sh

exec uvicorn src.main:app --host 0.0.0.0 --port 5002