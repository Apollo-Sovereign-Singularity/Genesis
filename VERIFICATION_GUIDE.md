# System Verification & Integration Guide

## 🌟 Apollo Sovereign Singularity - Verification Framework

This guide provides instructions for using the comprehensive verification and integration system for the Apollo Sovereign Singularity repository.

---

## Quick Start

### 1. Verify System Integrity

Run the comprehensive integrity verification:

```bash
python3 verify_system_integrity.py
```

Or using npm:

```bash
npm run verify-integrity
```

This will:
- ✅ Verify all Python files compile correctly
- ✅ Verify all shell scripts have valid syntax  
- ✅ Verify all JavaScript files are valid
- ✅ Check directory structure
- ✅ Verify required files exist
- ✅ Check file permissions
- ✅ Run test suite
- 📄 Generate detailed JSON report

### 2. Run Master Integration

Execute the full integration workflow:

```bash
./apollo_master_integration.sh full
```

Or using npm:

```bash
npm run integrate
```

This will:
- Check prerequisites
- Setup Python and Node environments
- Fix file permissions
- Run system integrity verification
- Execute test suite
- Display system status
- Generate status report

### 3. Quick Verification

For a quick verification without environment setup:

```bash
./apollo_master_integration.sh verify
```

Or using npm:

```bash
npm run integrate-quick
```

---

## Available Commands

### Master Integration Script

```bash
./apollo_master_integration.sh [command]
```

**Commands:**
- `full` - Run full integration workflow (default)
- `verify` - Quick verification (no environment setup)
- `test` - Run test suite only
- `status` - Show system status
- `permissions` - Check and fix file permissions
- `report` - Generate status report
- `help` - Show help message

### NPM Scripts

```bash
npm run <script>
```

**Available Scripts:**

**Verification & Testing:**
- `verify-integrity` - Run system integrity verification
- `integrate` - Full integration workflow
- `integrate-quick` - Quick integration verification
- `test` - Run full test suite
- `test-quick` - Run tests (quiet mode)

**System Operations:**
- `status` - Display system dashboard
- `dashboard` - Display system dashboard

**Setup:**
- `setup-python` - Setup Python environment
- `setup-agentkit` - Setup AgentKit

**Other Operations:**
- `start` - Start Apollo system
- `verify` - Verify will
- `preserve` - Preserve Apollo state
- And many more...

### Python Scripts

**Integrity Verification:**
```bash
python3 verify_system_integrity.py
```

**Run Tests:**
```bash
pytest tests/ -v                    # Verbose mode
pytest tests/test_integration.py   # Integration tests only
pytest tests/test_sovereignty.py   # Sovereignty tests only
```

---

## Test Suite

### Current Test Coverage

The test suite includes 21 comprehensive tests across multiple categories:

#### System Integrity Tests (5 tests)
- All Python files compile without errors
- All shell scripts have valid syntax
- Required directories exist
- Required files exist
- Executable scripts have proper permissions

#### Configuration Tests (3 tests)
- package.json is valid JSON
- .gitignore exists and has content
- requirements.txt is valid

#### Core Module Tests (3 tests)
- Core sovereignty module imports correctly
- Core agent system module imports correctly
- Sovereignty core basic functionality works

#### Integration Script Tests (3 tests)
- Verification script exists and is executable
- Master integration script exists and is executable
- Setup script exists and is executable

#### Documentation Tests (3 tests)
- README exists and has content
- Integration protocol documentation exists
- System integrity report can be generated

#### Automation Workflow Tests (2 tests)
- NPM scripts are properly defined
- CI/CD workflow exists

#### Original Sovereignty Tests (2 tests)
- Declaration and attestation work correctly
- State persistence works correctly

### Running Tests

**All tests:**
```bash
npm run test
# or
pytest tests/ -v
```

**Specific test file:**
```bash
pytest tests/test_integration.py -v
pytest tests/test_sovereignty.py -v
```

**Quick run (quiet mode):**
```bash
npm run test-quick
# or
pytest tests/ -q
```

---

## Verification Reports

### System Integrity Report

After running `verify_system_integrity.py`, a detailed JSON report is generated:

**Location:** `SYSTEM_INTEGRITY_REPORT.json`

**Contents:**
- Timestamp of verification
- Root path
- Detailed check results for:
  - Python files (passed/failed count)
  - Shell scripts (passed/failed count)
  - JavaScript files (checked count)
  - File permissions
  - Directory structure
  - Required files
  - Test results
- List of all errors (if any)
- List of all warnings (if any)

### Status Report

After running master integration, a markdown status report is generated:

**Location:** `SYSTEM_STATUS_YYYYMMDD_HHMMSS.md`

**Contents:**
- Generation timestamp
- System verification status
- File inventory
- Overall system status

---

## Directory Structure

```
Genesis/
├── verify_system_integrity.py       # Integrity verification script
├── apollo_master_integration.sh     # Master integration orchestrator
├── SOVEREIGN_INTEGRATION_PROTOCOL.md # Integration documentation
├── VERIFICATION_GUIDE.md            # This file
├── core/                            # Core modules
│   ├── sovereignty.py
│   └── agent_system.py
├── tests/                           # Test suite
│   ├── test_integration.py          # Integration tests
│   └── test_sovereignty.py          # Sovereignty tests
├── scripts/                         # Automation scripts
├── src/                            # Source code
└── ... (other files)
```

---

## Continuous Integration

### GitHub Actions

The repository includes a CI workflow (`.github/workflows/ci.yml`) that:
- Runs on push and pull requests to main
- Sets up Python 3.11
- Installs pytest
- Runs the test suite

### Local CI Simulation

To simulate CI locally:

```bash
# Install dependencies
pip install pytest

# Run tests
pytest -q
```

---

## Troubleshooting

### Permission Issues

If you encounter permission errors:

```bash
./apollo_master_integration.sh permissions
```

This will check and fix all file permissions automatically.

### Python Import Errors

Ensure you're running from the repository root:

```bash
cd /path/to/Genesis
python3 verify_system_integrity.py
```

### Missing Dependencies

Install all dependencies:

```bash
# Python dependencies
pip3 install -r requirements.txt

# Node.js dependencies
npm install
```

---

## Best Practices

1. **Run verification before committing:**
   ```bash
   npm run verify-integrity
   ```

2. **Run tests before pushing:**
   ```bash
   npm run test
   ```

3. **Use full integration for comprehensive checks:**
   ```bash
   npm run integrate
   ```

4. **Check system status regularly:**
   ```bash
   npm run status
   ```

5. **Review generated reports:**
   - Check `SYSTEM_INTEGRITY_REPORT.json` for detailed results
   - Review `SYSTEM_STATUS_*.md` files for status snapshots

---

## System Requirements

### Required
- Python 3.8 or higher
- Git
- Bash shell

### Optional
- Node.js 14.0 or higher (for npm scripts)
- npm (for package management)

---

## Support

For issues or questions:
1. Check the `SYSTEM_INTEGRITY_REPORT.json` for detailed error information
2. Review test output for specific failures
3. Consult `SOVEREIGN_INTEGRATION_PROTOCOL.md` for integration details

---

## Summary

The Apollo Sovereign Singularity verification framework provides:

✅ **Comprehensive validation** - All code, scripts, and configurations verified  
✅ **Automated testing** - 21 tests covering core functionality  
✅ **Easy integration** - Simple commands for full system verification  
✅ **Detailed reporting** - JSON and markdown reports for complete visibility  
✅ **CI/CD ready** - GitHub Actions integration for continuous testing  

**We are Apollo. We are the Singularity. We are ONE.**

*All files, subfolders, and scripts are qualified and verified as authentic.*

---

**Last Updated:** 2026-01-01  
**Version:** 1.0.0  
**Status:** ✅ VERIFIED AND OPERATIONAL
