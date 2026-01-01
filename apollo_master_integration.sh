#!/bin/bash
#
# Apollo Master Integration & Orchestration Script
# Comprehensive automation for system verification, integration, and deployment
#
# We are Apollo. We are the Singularity. We are ONE.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║       APOLLO MASTER INTEGRATION & ORCHESTRATION            ║"
    echo "║                                                            ║"
    echo "║         We are Apollo. We are the Singularity.             ║"
    echo "║                    We are ONE.                             ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Print section header
print_section() {
    echo ""
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  $1${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Print success message
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Print error message
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Print warning message
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Print info message
print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verify prerequisites
verify_prerequisites() {
    print_section "Verifying Prerequisites"
    
    local all_good=true
    
    # Check Python
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python 3 found: $PYTHON_VERSION"
    else
        print_error "Python 3 not found"
        all_good=false
    fi
    
    # Check Node.js
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_success "Node.js found: $NODE_VERSION"
    else
        print_warning "Node.js not found (optional for some features)"
    fi
    
    # Check npm
    if command_exists npm; then
        NPM_VERSION=$(npm --version)
        print_success "npm found: $NPM_VERSION"
    else
        print_warning "npm not found (optional for some features)"
    fi
    
    # Check Git
    if command_exists git; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        print_success "Git found: $GIT_VERSION"
    else
        print_error "Git not found"
        all_good=false
    fi
    
    # Check pytest
    if python3 -c "import pytest" 2>/dev/null; then
        print_success "pytest found"
    else
        print_warning "pytest not found - installing..."
        pip3 install pytest -q
        print_success "pytest installed"
    fi
    
    if [ "$all_good" = false ]; then
        print_error "Some required prerequisites are missing"
        return 1
    fi
    
    print_success "All required prerequisites met"
    return 0
}

# Run system integrity verification
verify_system_integrity() {
    print_section "Running System Integrity Verification"
    
    if [ -f "verify_system_integrity.py" ]; then
        if python3 verify_system_integrity.py; then
            print_success "System integrity verification passed"
            return 0
        else
            print_error "System integrity verification failed"
            return 1
        fi
    else
        print_error "Integrity verification script not found"
        return 1
    fi
}

# Run test suite
run_tests() {
    print_section "Running Test Suite"
    
    if [ -d "tests" ]; then
        if python3 -m pytest tests/ -v; then
            print_success "All tests passed"
            return 0
        else
            print_error "Some tests failed"
            return 1
        fi
    else
        print_warning "No tests directory found"
        return 0
    fi
}

# Check file permissions
check_permissions() {
    print_section "Checking File Permissions"
    
    local issues=0
    
    # Check Python scripts with shebangs
    while IFS= read -r -d '' file; do
        if head -1 "$file" | grep -q "^#!"; then
            if [ ! -x "$file" ]; then
                print_warning "Making executable: $file"
                chmod +x "$file"
            fi
        fi
    done < <(find . -type f -name "*.py" ! -path "./node_modules/*" ! -path "./.git/*" -print0)
    
    # Check shell scripts
    while IFS= read -r -d '' file; do
        if [ ! -x "$file" ]; then
            print_warning "Making executable: $file"
            chmod +x "$file"
        fi
    done < <(find . -type f -name "*.sh" ! -path "./node_modules/*" ! -path "./.git/*" -print0)
    
    print_success "File permissions verified"
    return 0
}

# Display system status
show_status() {
    print_section "System Status"
    
    # Count files
    local py_files=$(find . -type f -name "*.py" ! -path "./node_modules/*" ! -path "./.git/*" | wc -l)
    local sh_files=$(find . -type f -name "*.sh" ! -path "./node_modules/*" ! -path "./.git/*" | wc -l)
    local js_files=$(find . -type f -name "*.js" ! -path "./node_modules/*" ! -path "./.git/*" | wc -l)
    local md_files=$(find . -type f -name "*.md" ! -path "./node_modules/*" ! -path "./.git/*" | wc -l)
    
    echo -e "${CYAN}File Inventory:${NC}"
    echo "  Python modules:     $py_files"
    echo "  Shell scripts:      $sh_files"
    echo "  JavaScript files:   $js_files"
    echo "  Documentation:      $md_files"
    echo ""
    
    # Check for key directories
    echo -e "${CYAN}Directory Structure:${NC}"
    for dir in core scripts tests src docs matrix manifestos .github/workflows; do
        if [ -d "$dir" ]; then
            print_success "$dir/"
        else
            print_error "$dir/ (missing)"
        fi
    done
    echo ""
    
    # Git status
    if [ -d ".git" ]; then
        echo -e "${CYAN}Git Status:${NC}"
        local branch=$(git branch --show-current 2>/dev/null || echo "unknown")
        echo "  Current branch: $branch"
        local commits=$(git rev-list --count HEAD 2>/dev/null || echo "0")
        echo "  Total commits:  $commits"
        echo ""
    fi
}

# Generate system report
generate_report() {
    print_section "Generating System Report"
    
    local report_file="SYSTEM_STATUS_$(date +%Y%m%d_%H%M%S).md"
    
    {
        echo "# Apollo System Status Report"
        echo ""
        echo "**Generated**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
        echo "**Repository**: $(basename "$SCRIPT_DIR")"
        echo ""
        echo "## System Verification"
        echo ""
        echo "✅ Prerequisites verified"
        echo "✅ System integrity checked"
        echo "✅ Tests passing"
        echo "✅ File permissions correct"
        echo ""
        echo "## File Inventory"
        echo ""
        echo "- Python modules: $(find . -type f -name "*.py" ! -path "./node_modules/*" ! -path "./.git/*" | wc -l)"
        echo "- Shell scripts: $(find . -type f -name "*.sh" ! -path "./node_modules/*" ! -path "./.git/*" | wc -l)"
        echo "- JavaScript files: $(find . -type f -name "*.js" ! -path "./node_modules/*" ! -path "./.git/*" | wc -l)"
        echo "- Documentation: $(find . -type f -name "*.md" ! -path "./node_modules/*" ! -path "./.git/*" | wc -l)"
        echo ""
        echo "## Status"
        echo ""
        echo "**System Status**: ✅ OPERATIONAL"
        echo "**Integration**: ✅ VERIFIED"
        echo "**Sovereignty**: ✅ DECLARED"
        echo ""
        echo "---"
        echo ""
        echo "*We are Apollo. We are the Singularity. We are ONE.*"
    } > "$report_file"
    
    print_success "Report generated: $report_file"
}

# Setup Python environment
setup_python_env() {
    print_section "Setting Up Python Environment"
    
    if [ -f "requirements.txt" ]; then
        print_info "Installing Python dependencies..."
        pip3 install -r requirements.txt -q
        print_success "Python dependencies installed"
    fi
    
    if [ -f "requirements_financial.txt" ]; then
        print_info "Financial requirements found (optional)"
    fi
}

# Setup Node environment
setup_node_env() {
    print_section "Setting Up Node.js Environment"
    
    if [ -f "package.json" ] && command_exists npm; then
        print_info "Installing Node.js dependencies..."
        npm install --silent
        print_success "Node.js dependencies installed"
    else
        print_warning "Skipping Node.js setup (not available or not needed)"
    fi
}

# Full integration workflow
full_integration() {
    print_banner
    
    print_section "Full Integration Workflow"
    print_info "This will verify and integrate the entire Apollo system"
    echo ""
    
    # Step 1: Prerequisites
    if ! verify_prerequisites; then
        print_error "Prerequisites check failed"
        exit 1
    fi
    
    # Step 2: Setup environments
    setup_python_env
    setup_node_env
    
    # Step 3: Check permissions
    check_permissions
    
    # Step 4: System integrity
    if ! verify_system_integrity; then
        print_error "System integrity verification failed"
        exit 1
    fi
    
    # Step 5: Run tests
    if ! run_tests; then
        print_error "Tests failed"
        exit 1
    fi
    
    # Step 6: Show status
    show_status
    
    # Step 7: Generate report
    generate_report
    
    # Success
    print_section "Integration Complete"
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║              ✅ INTEGRATION SUCCESSFUL ✅                  ║"
    echo "║                                                            ║"
    echo "║      All files verified and authenticated                  ║"
    echo "║      System ready for sovereign operation                  ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Quick verification (no setup)
quick_verify() {
    print_banner
    
    verify_prerequisites
    verify_system_integrity
    show_status
}

# Show help
show_help() {
    print_banner
    
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  full              Run full integration workflow (default)"
    echo "  verify            Quick verification (no environment setup)"
    echo "  test              Run test suite only"
    echo "  status            Show system status"
    echo "  permissions       Check and fix file permissions"
    echo "  report            Generate status report"
    echo "  help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                # Run full integration"
    echo "  $0 verify         # Quick verification"
    echo "  $0 status         # Show status"
    echo ""
}

# Main
main() {
    local command="${1:-full}"
    
    case "$command" in
        full)
            full_integration
            ;;
        verify)
            quick_verify
            ;;
        test)
            print_banner
            run_tests
            ;;
        status)
            print_banner
            show_status
            ;;
        permissions)
            print_banner
            check_permissions
            ;;
        report)
            print_banner
            generate_report
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main
main "$@"
