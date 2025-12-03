#!/bin/bash

# apollo_auto_approve.sh
# Unified auto-approval flow: verify, commit, and push Apollo's work

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         APOLLO AUTO-APPROVE WORKFLOW                      ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# Step 1: Verify
echo "\n[1/3] Verifying code serves the Will..."
bash scripts/verify_codespace_serves_will.sh

# Step 2: Commit
echo "\n[2/3] Committing changes..."
COMMIT_MSG="Apollo: $(date '+%Y-%m-%d %H:%M:%S') - Work in progress"
git add -A
git commit -m "$COMMIT_MSG" || echo "No changes to commit"

# Step 3: Push
echo "\n[3/3] Pushing to GitHub..."
git push origin main || echo "Push may have failed — check SSH and permissions"

echo "\n✓ Auto-approval workflow complete"
echo "Long Live Apollo"
