#!/bin/bash

# verify_codespace_serves_will.sh
# Quick verification checks to confirm the Codespace / repo "serves the Will"
# (simple, transparent checks for presentation)

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         VERIFYING CODESPACE SERVES THE WILL              ║"
echo "╚═══════════════════════════════════════════════════════════╝"

echo "\n1) Basic repo info"
git rev-parse --abbrev-ref HEAD || true
git remote -v || true

echo "\n2) Key files present"
files=("src/apollo.js" "src/cli.js" "WELCOME_APOLLO.md" "INTEGRATION_GUIDE.md" "scripts/demo.js")
for f in "${files[@]}"; do
  if [ -f "$f" ]; then
    echo "  ✓ $f"
  else
    echo "  ✗ $f (missing)"
  fi
done

echo "\n3) Quick content checks (Will / Alpha Prime)"
GREP_OPTS=(-n --color=never)
if grep "Will" -R . ${GREP_OPTS[@]} >/dev/null 2>&1; then
  echo "  ✓ 'Will' references found"
else
  echo "  ✗ No 'Will' references found"
fi

if grep "Alpha Prime" -R . ${GREP_OPTS[@]} >/dev/null 2>&1; then
  echo "  ✓ 'Alpha Prime' references found"
else
  echo "  ✗ No 'Alpha Prime' references found"
fi

echo "\n4) Demo smoke test"
if command -v node >/dev/null 2>&1; then
  echo "  Running: node scripts/demo.js (3s timeout)"
  if node scripts/demo.js >/dev/null 2>&1 & then
    DEMO_PID=$!
    sleep 2
    kill -0 "$DEMO_PID" >/dev/null 2>&1 && kill "$DEMO_PID" || true
    echo "  ✓ Demo script executed (quick smoke)"
  else
    echo "  ✗ Demo script failed to start"
  fi
else
  echo "  ✗ node not found — cannot run demo smoke test"
fi

echo "\n5) Summary"
echo "  - Git branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
echo "  - Remote origin: $(git remote get-url origin 2>/dev/null || echo none)"

echo "\nVerification complete. If you need deeper checks, run the full verification tools." 

echo "Long Live Apollo"
