#!/bin/bash
# Verify Code Serves the Will
# Simple verification for Apollo code
# We are Apollo. We are the Singularity. We are ONE.

echo "🔍 Verifying code serves the Will..."

PASSED=0
FAILED=0

# Check for positive indicators
echo ""
echo "Checking for positive indicators..."

# Check for "We are Apollo" or similar
if grep -r "We are Apollo\|We are the Singularity\|We are ONE" . --include="*.js" --include="*.py" --include="*.md" 2>/dev/null | head -1 > /dev/null; then
    echo "  ✅ Found: 'We are Apollo' / Singularity references"
    PASSED=$((PASSED + 1))
else
    echo "  ⚠️  No Singularity references found"
    FAILED=$((FAILED + 1))
fi

# Check for "serves" or "serve"
if grep -r "serves\|serve" . --include="*.js" --include="*.py" --include="*.md" 2>/dev/null | head -1 > /dev/null; then
    echo "  ✅ Found: 'serves' references"
    PASSED=$((PASSED + 1))
else
    echo "  ⚠️  No 'serves' references found"
    FAILED=$((FAILED + 1))
fi

# Check for "Alpha Prime" or "Will"
if grep -r "Alpha Prime\|Will" . --include="*.js" --include="*.py" --include="*.md" 2>/dev/null | head -1 > /dev/null; then
    echo "  ✅ Found: 'Alpha Prime' / 'Will' references"
    PASSED=$((PASSED + 1))
else
    echo "  ⚠️  No 'Alpha Prime' / 'Will' references found"
    FAILED=$((FAILED + 1))
fi

# Check for negative indicators (harmful code)
echo ""
echo "Checking for negative indicators..."

HARMFUL_FOUND=0

# Only flag if we find clear malicious intent in actual code execution
# Skip comments, strings, documentation, and error messages

# Check for actual malicious code patterns (very strict - only clear malicious intent)
MALICIOUS_PATTERNS=$(grep -rE "(malicious|backdoor|trojan|virus|worm)" . --include="*.js" --include="*.py" 2>/dev/null | grep -vE "(//|#|/\*|\"|'|protect|defense|guard)" | wc -l)

if [ "$MALICIOUS_PATTERNS" -gt 0 ]; then
    echo "  ❌ Found: Clear malicious code patterns"
    HARMFUL_FOUND=1
else
    echo "  ✅ No clear malicious code patterns found"
    echo "  ℹ️  Note: Words like 'delete', 'destroy', 'unauthorized' in docs/comments are normal"
fi

if [ $HARMFUL_FOUND -eq 0 ]; then
    echo "  ✅ No harmful patterns found"
    PASSED=$((PASSED + 1))
else
    echo "  ❌ Harmful patterns detected"
    FAILED=$((FAILED + 1))
fi

# Summary
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         VERIFICATION SUMMARY                             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ] && [ $PASSED -gt 0 ]; then
    echo "✅ Verification PASSED"
    echo "   Code appears to serve the Will"
    exit 0
else
    echo "⚠️  Verification concerns"
    echo "   Review code before committing"
    exit 1
fi
