#!/bin/bash

# present_apollo.sh
# Present Apollo: optionally read the ceremonial welcome and run the demo

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SAY_CMD=""
if command -v espeak >/dev/null 2>&1; then
  SAY_CMD="espeak -v en-uk"
elif command -v say >/dev/null 2>&1; then
  SAY_CMD="say"
fi

if [ "$1" = "--read" ] || [ "$1" = "-r" ]; then
  echo "Reading WELCOME_APOLLO.md"
  if [ -n "$SAY_CMD" ]; then
    cat WELCOME_APOLLO.md | $SAY_CMD
  else
    cat WELCOME_APOLLO.md
  fi
fi

echo "Running demo sequence"
if command -v node >/dev/null 2>&1; then
  node scripts/demo.js
else
  echo "Node.js is not installed or not on PATH — cannot run demo."
  exit 1
fi

echo "Presentation complete. Long Live Apollo"
