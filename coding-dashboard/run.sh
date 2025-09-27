#!/bin/bash

# Personal Coding Dashboard Runner
# Uses uv for super fast dependency management

echo "🚀 Starting Personal Coding Dashboard..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Run the dashboard with uv (automatically handles dependencies and venv)
echo "🎯 Launching dashboard with uv..."
uv run main.py
