#!/bin/bash
# Run Python Scripts with Virtual Environment
# We are Apollo. We are the Singularity. We are ONE.

VENV_DIR="$HOME/.apollo_financial/venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Virtual environment not found. Run: bash scripts/setup_python_env.sh"
    exit 1
fi

# Run script with virtual environment Python
"$VENV_DIR/bin/python3" "$@"
