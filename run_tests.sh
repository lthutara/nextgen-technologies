#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Running API tests..."
PYTHONPATH=$(pwd) pytest tests/test_api.py

echo "Running Curation Workflow tests..."
PYTHONPATH=$(pwd) pytest tests/test_curation_workflow.py

echo "All tests passed!"
