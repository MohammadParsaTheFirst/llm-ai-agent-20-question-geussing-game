#!/bin/bash
# run.sh

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Run the application
python main.py
