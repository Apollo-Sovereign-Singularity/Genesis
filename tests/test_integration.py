"""
Comprehensive System Integration Tests
Tests for the Apollo Sovereign Singularity system integration
"""

import json
import subprocess
import sys
from pathlib import Path
import pytest


class TestSystemIntegrity:
    """Test system integrity and file validation"""
    
    def test_all_python_files_compile(self):
        """Verify all Python files compile without syntax errors"""
        root = Path(__file__).parent.parent
        python_files = [f for f in root.rglob("*.py") 
                       if 'node_modules' not in str(f) and '.git' not in str(f)]
        
        failed_files = []
        for py_file in python_files:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(py_file)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                failed_files.append((py_file, result.stderr))
        
        assert len(failed_files) == 0, f"Files with syntax errors: {failed_files}"
    
    def test_all_shell_scripts_valid(self):
        """Verify all shell scripts have valid syntax"""
        root = Path(__file__).parent.parent
        shell_files = [f for f in root.rglob("*.sh") 
                      if 'node_modules' not in str(f) and '.git' not in str(f)]
        
        failed_files = []
        for sh_file in shell_files:
            result = subprocess.run(
                ["bash", "-n", str(sh_file)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                failed_files.append((sh_file, result.stderr))
        
        assert len(failed_files) == 0, f"Scripts with syntax errors: {failed_files}"
    
    def test_required_directories_exist(self):
        """Verify required directories exist"""
        root = Path(__file__).parent.parent
        required_dirs = [
            "core",
            "scripts",
            "tests",
            "src",
            "docs",
            "matrix",
            ".github/workflows"
        ]
        
        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = root / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
        
        assert len(missing_dirs) == 0, f"Missing directories: {missing_dirs}"
    
    def test_required_files_exist(self):
        """Verify required configuration files exist"""
        root = Path(__file__).parent.parent
        required_files = [
            "README.md",
            "package.json",
            "requirements.txt",
            ".gitignore",
            "LICENSE"
        ]
        
        missing_files = []
        for file_name in required_files:
            file_path = root / file_name
            if not file_path.exists():
                missing_files.append(file_name)
        
        assert len(missing_files) == 0, f"Missing files: {missing_files}"
    
    def test_executable_scripts_have_permissions(self):
        """Verify executable scripts have proper permissions"""
        root = Path(__file__).parent.parent
        
        # Check Python scripts with shebangs
        python_files = [f for f in root.rglob("*.py") 
                       if 'node_modules' not in str(f) and '.git' not in str(f)]
        
        missing_permissions = []
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline()
                    if first_line.startswith('#!'):
                        # File has shebang, should be executable
                        import os
                        if not os.access(py_file, os.X_OK):
                            missing_permissions.append(str(py_file))
            except (UnicodeDecodeError, FileNotFoundError, PermissionError):
                pass
        
        # All shell scripts should be executable
        shell_files = [f for f in root.rglob("*.sh") 
                      if 'node_modules' not in str(f) and '.git' not in str(f)]
        
        import os
        for sh_file in shell_files:
            if not os.access(sh_file, os.X_OK):
                missing_permissions.append(str(sh_file))
        
        assert len(missing_permissions) == 0, f"Files missing execute permissions: {missing_permissions}"


class TestConfigurationFiles:
    """Test configuration file validity"""
    
    def test_package_json_valid(self):
        """Verify package.json is valid JSON"""
        root = Path(__file__).parent.parent
        package_json = root / "package.json"
        
        assert package_json.exists(), "package.json not found"
        
        with open(package_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "name" in data, "package.json missing 'name' field"
        assert "version" in data, "package.json missing 'version' field"
        assert "scripts" in data, "package.json missing 'scripts' field"
    
    def test_gitignore_exists(self):
        """Verify .gitignore exists and has content"""
        root = Path(__file__).parent.parent
        gitignore = root / ".gitignore"
        
        assert gitignore.exists(), ".gitignore not found"
        
        content = gitignore.read_text(encoding='utf-8')
        assert len(content) > 0, ".gitignore is empty"
        assert "node_modules" in content or "__pycache__" in content, ".gitignore missing common patterns"
    
    def test_requirements_txt_valid(self):
        """Verify requirements.txt is readable"""
        root = Path(__file__).parent.parent
        requirements = root / "requirements.txt"
        
        assert requirements.exists(), "requirements.txt not found"
        
        content = requirements.read_text(encoding='utf-8')
        assert len(content) > 0, "requirements.txt is empty"


class TestCoreModules:
    """Test core module functionality"""
    
    def test_core_sovereignty_import(self):
        """Verify core sovereignty module can be imported"""
        from core.sovereignty import SovereigntyCore
        
        assert SovereigntyCore is not None
    
    def test_core_agent_system_import(self):
        """Verify core agent system module can be imported"""
        from core.agent_system import AgentManager
        
        assert AgentManager is not None
    
    def test_sovereignty_core_basic_functionality(self):
        """Test basic SovereigntyCore functionality"""
        from core.sovereignty import SovereigntyCore
        
        sc = SovereigntyCore()
        assert sc.name == "Apollo"
        assert sc.declared is False
        
        msg = sc.declare()
        assert sc.declared is True
        assert "Apollo" in msg
        
        attestation = sc.attest()
        assert attestation["name"] == "Apollo"
        assert attestation["declared"] is True


class TestIntegrationScripts:
    """Test integration script presence and validity"""
    
    def test_verification_script_exists(self):
        """Verify system integrity verification script exists"""
        root = Path(__file__).parent.parent
        script = root / "verify_system_integrity.py"
        
        assert script.exists(), "verify_system_integrity.py not found"
        assert script.stat().st_mode & 0o111, "verification script not executable"
    
    def test_master_integration_script_exists(self):
        """Verify master integration script exists"""
        root = Path(__file__).parent.parent
        script = root / "apollo_master_integration.sh"
        
        assert script.exists(), "apollo_master_integration.sh not found"
        assert script.stat().st_mode & 0o111, "master integration script not executable"
    
    def test_setup_script_exists(self):
        """Verify setup script exists"""
        root = Path(__file__).parent.parent
        script = root / "setup_apollo_singularity.sh"
        
        assert script.exists(), "setup_apollo_singularity.sh not found"
        assert script.stat().st_mode & 0o111, "setup script not executable"


class TestDocumentation:
    """Test documentation completeness"""
    
    def test_readme_exists(self):
        """Verify README.md exists and has content"""
        root = Path(__file__).parent.parent
        readme = root / "README.md"
        
        assert readme.exists(), "README.md not found"
        
        content = readme.read_text(encoding='utf-8')
        assert len(content) > 100, "README.md is too short"
        assert "Apollo" in content or "Sovereign" in content, "README missing project name"
    
    def test_integration_protocol_exists(self):
        """Verify integration protocol documentation exists"""
        root = Path(__file__).parent.parent
        protocol = root / "SOVEREIGN_INTEGRATION_PROTOCOL.md"
        
        assert protocol.exists(), "SOVEREIGN_INTEGRATION_PROTOCOL.md not found"
        
        content = protocol.read_text(encoding='utf-8')
        assert len(content) > 100, "Integration protocol is too short"
    
    def test_system_integrity_report_can_be_generated(self):
        """Verify system integrity report can be generated"""
        root = Path(__file__).parent.parent
        report_files = list(root.glob("SYSTEM_INTEGRITY_REPORT.json"))
        
        # Report should exist (created by verification script)
        assert len(report_files) > 0, "No system integrity report found"


class TestAutomationWorkflow:
    """Test automation and workflow scripts"""
    
    def test_npm_scripts_defined(self):
        """Verify npm scripts are properly defined"""
        root = Path(__file__).parent.parent
        package_json = root / "package.json"
        
        with open(package_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        scripts = data.get("scripts", {})
        
        # Check for key automation scripts
        expected_scripts = ["start", "verify", "status"]
        for script_name in expected_scripts:
            assert script_name in scripts, f"Missing npm script: {script_name}"
    
    def test_ci_workflow_exists(self):
        """Verify CI/CD workflow configuration exists"""
        root = Path(__file__).parent.parent
        ci_workflow = root / ".github" / "workflows" / "ci.yml"
        
        assert ci_workflow.exists(), "CI workflow not found"
        
        content = ci_workflow.read_text(encoding='utf-8')
        assert "test" in content.lower() or "pytest" in content.lower(), "CI workflow missing test step"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
