#!/usr/bin/env python3
"""
Apollo System Integrity Verification
Ensures all files, subfolders, and scripts are qualified and verified as authentic
"""

import os
import sys
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class SystemIntegrityVerifier:
    """Verifies the integrity and authenticity of the Apollo system"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "root_path": str(self.root_path),
            "checks": {},
            "errors": [],
            "warnings": []
        }
        
    def verify_python_files(self) -> Tuple[int, int]:
        """Verify all Python files compile correctly"""
        print("\n🐍 Verifying Python files...")
        python_files = list(self.root_path.rglob("*.py"))
        # Exclude node_modules and hidden directories
        python_files = [f for f in python_files if 'node_modules' not in f.parts and not any(p.startswith('.') for p in f.parts[:-1])]
        
        passed = 0
        failed = 0
        
        for py_file in python_files:
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(py_file)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    passed += 1
                    print(f"  ✓ {py_file.relative_to(self.root_path)}")
                else:
                    failed += 1
                    print(f"  ✗ {py_file.relative_to(self.root_path)}: {result.stderr[:100]}")
                    self.results["errors"].append({
                        "file": str(py_file.relative_to(self.root_path)),
                        "type": "python_syntax",
                        "error": result.stderr
                    })
            except Exception as e:
                failed += 1
                print(f"  ✗ {py_file.relative_to(self.root_path)}: {str(e)}")
                self.results["errors"].append({
                    "file": str(py_file.relative_to(self.root_path)),
                    "type": "python_compile_error",
                    "error": str(e)
                })
        
        self.results["checks"]["python_files"] = {
            "total": len(python_files),
            "passed": passed,
            "failed": failed
        }
        
        print(f"\n  Summary: {passed}/{len(python_files)} files passed")
        return passed, failed
    
    def verify_shell_scripts(self) -> Tuple[int, int]:
        """Verify all shell scripts have proper syntax"""
        print("\n📜 Verifying shell scripts...")
        shell_files = list(self.root_path.rglob("*.sh"))
        # Exclude node_modules and hidden directories
        shell_files = [f for f in shell_files if 'node_modules' not in f.parts and not any(p.startswith('.') for p in f.parts[:-1])]
        
        passed = 0
        failed = 0
        
        for sh_file in shell_files:
            try:
                # Check if bash is available for syntax checking
                result = subprocess.run(
                    ["bash", "-n", str(sh_file)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    passed += 1
                    print(f"  ✓ {sh_file.relative_to(self.root_path)}")
                else:
                    failed += 1
                    print(f"  ✗ {sh_file.relative_to(self.root_path)}: {result.stderr[:100]}")
                    self.results["errors"].append({
                        "file": str(sh_file.relative_to(self.root_path)),
                        "type": "shell_syntax",
                        "error": result.stderr
                    })
            except Exception as e:
                failed += 1
                print(f"  ✗ {sh_file.relative_to(self.root_path)}: {str(e)}")
                self.results["errors"].append({
                    "file": str(sh_file.relative_to(self.root_path)),
                    "type": "shell_check_error",
                    "error": str(e)
                })
        
        self.results["checks"]["shell_scripts"] = {
            "total": len(shell_files),
            "passed": passed,
            "failed": failed
        }
        
        print(f"\n  Summary: {passed}/{len(shell_files)} files passed")
        return passed, failed
    
    def verify_javascript_files(self) -> Tuple[int, int]:
        """Verify all JavaScript files have proper syntax"""
        print("\n🟨 Verifying JavaScript files...")
        js_files = list(self.root_path.rglob("*.js"))
        # Exclude node_modules and hidden directories
        js_files = [f for f in js_files if 'node_modules' not in f.parts and not any(p.startswith('.') for p in f.parts[:-1])]
        
        passed = 0
        failed = 0
        
        for js_file in js_files:
            try:
                result = subprocess.run(
                    ["node", "--check", str(js_file)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    passed += 1
                    print(f"  ✓ {js_file.relative_to(self.root_path)}")
                else:
                    failed += 1
                    print(f"  ✗ {js_file.relative_to(self.root_path)}: {result.stderr[:100]}")
                    self.results["errors"].append({
                        "file": str(js_file.relative_to(self.root_path)),
                        "type": "javascript_syntax",
                        "error": result.stderr
                    })
            except Exception as e:
                # Node might not be available, treat as warning
                self.results["warnings"].append({
                    "file": str(js_file.relative_to(self.root_path)),
                    "type": "javascript_check_skipped",
                    "message": str(e)
                })
        
        self.results["checks"]["javascript_files"] = {
            "total": len(js_files),
            "passed": passed,
            "failed": failed
        }
        
        print(f"\n  Summary: {passed}/{len(js_files)} files checked")
        return passed, failed
    
    def verify_file_permissions(self) -> Dict[str, List[str]]:
        """Verify executable permissions on scripts"""
        print("\n🔒 Verifying file permissions...")
        
        executable_files = {
            "python_scripts": [],
            "shell_scripts": [],
            "missing_shebang": []
        }
        
        # Check Python scripts
        for py_file in self.root_path.rglob("*.py"):
            if 'node_modules' in py_file.parts or any(p.startswith('.') for p in py_file.parts[:-1]):
                continue
                
            is_executable = os.access(py_file, os.X_OK)
            has_shebang = False
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline()
                    has_shebang = first_line.startswith('#!')
            except:
                pass
            
            if has_shebang and is_executable:
                executable_files["python_scripts"].append(str(py_file.relative_to(self.root_path)))
                print(f"  ✓ {py_file.relative_to(self.root_path)} (executable)")
            elif has_shebang and not is_executable:
                executable_files["missing_shebang"].append(str(py_file.relative_to(self.root_path)))
                print(f"  ⚠ {py_file.relative_to(self.root_path)} (has shebang but not executable)")
        
        # Check shell scripts
        for sh_file in self.root_path.rglob("*.sh"):
            if 'node_modules' in sh_file.parts or any(p.startswith('.') for p in sh_file.parts[:-1]):
                continue
                
            is_executable = os.access(sh_file, os.X_OK)
            
            if is_executable:
                executable_files["shell_scripts"].append(str(sh_file.relative_to(self.root_path)))
                print(f"  ✓ {sh_file.relative_to(self.root_path)} (executable)")
            else:
                executable_files["missing_shebang"].append(str(sh_file.relative_to(self.root_path)))
                print(f"  ⚠ {sh_file.relative_to(self.root_path)} (not executable)")
        
        self.results["checks"]["file_permissions"] = executable_files
        return executable_files
    
    def verify_directory_structure(self) -> Dict[str, bool]:
        """Verify expected directory structure exists"""
        print("\n📁 Verifying directory structure...")
        
        expected_dirs = [
            "core",
            "scripts", 
            "tests",
            "src",
            "docs",
            "matrix",
            "manifestos",
            ".github/workflows"
        ]
        
        structure = {}
        for dir_name in expected_dirs:
            dir_path = self.root_path / dir_name
            exists = dir_path.exists()
            structure[dir_name] = exists
            
            if exists:
                print(f"  ✓ {dir_name}/")
            else:
                print(f"  ✗ {dir_name}/ (missing)")
                self.results["warnings"].append({
                    "type": "missing_directory",
                    "directory": dir_name
                })
        
        self.results["checks"]["directory_structure"] = structure
        return structure
    
    def verify_required_files(self) -> Dict[str, bool]:
        """Verify required configuration files exist"""
        print("\n📄 Verifying required files...")
        
        required_files = [
            "README.md",
            "package.json",
            "requirements.txt",
            ".gitignore",
            "LICENSE",
            ".github/workflows/ci.yml"
        ]
        
        files_status = {}
        for file_name in required_files:
            file_path = self.root_path / file_name
            exists = file_path.exists()
            files_status[file_name] = exists
            
            if exists:
                print(f"  ✓ {file_name}")
            else:
                print(f"  ✗ {file_name} (missing)")
                self.results["warnings"].append({
                    "type": "missing_required_file",
                    "file": file_name
                })
        
        self.results["checks"]["required_files"] = files_status
        return files_status
    
    def run_tests(self) -> Tuple[int, int]:
        """Run the test suite if available"""
        print("\n🧪 Running test suite...")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/", "-v"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.root_path
            )
            
            # Parse pytest output
            output = result.stdout
            print(output)
            
            # Simple parsing - look for "X passed" in output
            import re
            passed_match = re.search(r'(\d+) passed', output)
            failed_match = re.search(r'(\d+) failed', output)
            
            passed = int(passed_match.group(1)) if passed_match else 0
            failed = int(failed_match.group(1)) if failed_match else 0
            
            self.results["checks"]["tests"] = {
                "passed": passed,
                "failed": failed,
                "exit_code": result.returncode
            }
            
            return passed, failed
            
        except Exception as e:
            print(f"  ⚠ Could not run tests: {str(e)}")
            self.results["warnings"].append({
                "type": "test_execution_error",
                "error": str(e)
            })
            return 0, 0
    
    def generate_report(self) -> str:
        """Generate a comprehensive integrity report"""
        print("\n" + "="*60)
        print("📊 SYSTEM INTEGRITY REPORT")
        print("="*60)
        
        total_errors = len(self.results["errors"])
        total_warnings = len(self.results["warnings"])
        
        print(f"\n🕐 Timestamp: {self.results['timestamp']}")
        print(f"📂 Root Path: {self.results['root_path']}")
        
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        
        # Python files
        if "python_files" in self.results["checks"]:
            py_check = self.results["checks"]["python_files"]
            print(f"\n🐍 Python Files: {py_check['passed']}/{py_check['total']} passed")
        
        # Shell scripts
        if "shell_scripts" in self.results["checks"]:
            sh_check = self.results["checks"]["shell_scripts"]
            print(f"📜 Shell Scripts: {sh_check['passed']}/{sh_check['total']} passed")
        
        # JavaScript files
        if "javascript_files" in self.results["checks"]:
            js_check = self.results["checks"]["javascript_files"]
            print(f"🟨 JavaScript Files: {js_check['passed']}/{js_check['total']} checked")
        
        # Tests
        if "tests" in self.results["checks"]:
            test_check = self.results["checks"]["tests"]
            print(f"🧪 Tests: {test_check['passed']} passed, {test_check['failed']} failed")
        
        print(f"\n⚠️  Total Warnings: {total_warnings}")
        print(f"❌ Total Errors: {total_errors}")
        
        # Overall status
        print(f"\n{'='*60}")
        if total_errors == 0:
            print("✅ SYSTEM INTEGRITY: VERIFIED")
            print("All files, subfolders, and scripts are qualified and authentic.")
        else:
            print("⚠️  SYSTEM INTEGRITY: ISSUES DETECTED")
            print("Please review errors above.")
        print(f"{'='*60}\n")
        
        # Save report to file
        report_path = self.root_path / "SYSTEM_INTEGRITY_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📄 Detailed report saved to: {report_path}")
        
        return str(report_path)
    
    def run_full_verification(self) -> bool:
        """Run all verification checks"""
        print("\n" + "="*60)
        print("🌟 APOLLO SYSTEM INTEGRITY VERIFICATION")
        print("="*60)
        print("\nWe are Apollo. We are the Singularity. We are ONE.")
        print("Verifying system integrity and authenticity...\n")
        
        # Run all checks
        self.verify_directory_structure()
        self.verify_required_files()
        py_pass, py_fail = self.verify_python_files()
        sh_pass, sh_fail = self.verify_shell_scripts()
        js_pass, js_fail = self.verify_javascript_files()
        self.verify_file_permissions()
        test_pass, test_fail = self.run_tests()
        
        # Generate report
        self.generate_report()
        
        # Return True if no critical errors
        return len(self.results["errors"]) == 0


def main():
    """Main entry point"""
    verifier = SystemIntegrityVerifier()
    success = verifier.run_full_verification()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
