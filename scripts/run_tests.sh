#!/bin/bash
set -e
pytest tests/ --cov=app --cov-report=term-missing
