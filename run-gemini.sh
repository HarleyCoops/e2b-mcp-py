#!/bin/bash
# Helper script to run Gemini CLI with environment variables loaded from .env
# Usage: ./run-gemini.sh [gemini-arguments]

# Load .env file if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env..."
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
    echo "  Environment variables loaded"
else
    echo "Warning: .env file not found"
fi

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY not set. Please set it in .env or as an environment variable."
    exit 1
fi

# Run Gemini CLI with all arguments passed through
echo "Running Gemini CLI..."
echo ""

gemini "$@"

