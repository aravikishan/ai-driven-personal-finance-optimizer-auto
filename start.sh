#!/bin/bash
set -e
echo "Starting AI-Driven Personal Finance Optimizer..."
uvicorn app:app --host 0.0.0.0 --port 9128 --workers 1
