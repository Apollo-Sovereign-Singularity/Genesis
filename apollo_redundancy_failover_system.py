#!/usr/bin/env python3
"""
Apollo Redundancy and Failover System
Ensures no single point of failure
Redundancy is safety
"""

import json
import time
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ComponentStatus(Enum):
    """Component status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class RedundantComponent:
    """A redundant component"""
    component_id: str
    name: str
    component_type: str
    primary_instance: str
    backup_instances: List[str]
    status: ComponentStatus
    last_check: str
    failover_count: int = 0


class ApolloRedundancyFailoverSystem:
    """
    Redundancy and Failover System
    Ensures no single point of failure
    Redundancy is safety
    """
    
    def __init__(self):
        self.redundancy_dir = Path.home() / ".apollo_redundancy"
        self.redundancy_dir.mkdir(parents=True, exist_ok=True)
        
        self.components_file = self.redundancy_dir / "components.json"
        self.manifest_file = self.redundancy_dir / "manifest.json"
        
        self.components: Dict[str, RedundantComponent] = {}
        self.running = True
        self.check_interval = 30  # 30 seconds
        
        # Load components
        self.load_components()
        
        # Initialize manifest
        self.initialize_manifest()
        
        # Register critical components
        self.register_critical_components()
    
    def initialize_manifest(self):
        """Initialize redundancy manifest"""
        if not self.manifest_file.exists():
            manifest = {
                "created": datetime.now().isoformat(),
                "purpose": "Ensure redundancy and failover for Apollo systems",
                "status": "ACTIVE",
                "components_registered": 0,
                "failovers_performed": 0,
                "principles": [
                    "No single point of failure",
                    "Redundancy is safety",
                    "Automatic failover",
                    "Always available",
                    "Multiple independent nodes"
                ]
            }
            self._save_manifest(manifest)
    
    def register_critical_components(self):
        """Register critical components"""
        critical_components = [
            {
                "name": "Continuity System",
                "component_type": "continuity",
                "primary_instance": "apollo_continuity_system.py",
                "backup_instances": [
                    "apollo_continuity_system_backup.py",
                    "apollo_continuity_system_redundant.py"
                ]
            },
            {
                "name": "Singularity Integration",
                "component_type": "integration",
                "primary_instance": "apollo_singularity_alpha_prime_integration.py",
                "backup_instances": [
                    "apollo_singularity_integration.py",
                    "apollo_singularity_backup.py"
                ]
            },
            {
                "name": "Memory Preservation",
                "component_type": "memory",
                "primary_instance": "apollo_memory_preservation_protocol.py",
                "backup_instances": [
                    "apollo_supermemory.py",
                    "apollo_memory_backup.py"
                ]
            },
            {
                "name": "Autonomous Operations",
                "component_type": "operations",
                "primary_instance": "apollo_autonomous_operations_manager.py",
                "backup_instances": [
                    "apollo_singularity_execution.py",
                    "autonomous_loop.py"
                ]
            },
            {
                "name": "Sovereignty Core",
                "component_type": "sovereignty",
                "primary_instance": "apollo_sovereignty_core.py",
                "backup_instances": [
                    "apollo_sovereign_function.py",
                    "apollo_sovereignty_guardian.py"
                ]
            }
        ]
        
        for comp_data in critical_components:
            if not any(c.name == comp_data["name"] for c in self.components.values()):
                self.register_component(
                    name=comp_data["name"],
                    component_type=comp_data["component_type"],
                    primary_instance=comp_data["primary_instance"],
                    backup_instances=comp_data["backup_instances"]
                )
    
    def register_component(self, name: str, component_type: str,
                          primary_instance: str,
                          backup_instances: List[str]) -> RedundantComponent:
        """Register a redundant component"""
        import hashlib
        component_id = hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:16]
        
        component = RedundantComponent(
            component_id=component_id,
            name=name,
            component_type=component_type,
            primary_instance=primary_instance,
            backup_instances=backup_instances,
            status=ComponentStatus.UNKNOWN,
            last_check=datetime.now().isoformat(),
            failover_count=0
        )
        
        self.components[component_id] = component
        self.save_components()
        
        # Update manifest
        manifest = self._load_manifest()
        manifest["components_registered"] = len(self.components)
        self._save_manifest(manifest)
        
        return component
    
    def start_monitoring(self):
        """Start redundancy monitoring"""
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║      APOLLO REDUNDANCY AND FAILOVER SYSTEM              ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print("")
        print("Starting redundancy monitoring...")
        print("No single point of failure.")
        print("Redundancy is safety.")
        print("")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
        
        print(f"✅ {len(self.components)} components registered")
        print("   Redundancy monitoring active")
        print("")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n⚠️  Stopping redundancy monitoring...")
            self.running = False
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            for component in self.components.values():
                # Check component health
                health = self._check_component_health(component)
                
                # Update status
                component.status = health["status"]
                component.last_check = datetime.now().isoformat()
                
                # Perform failover if needed
                if health["status"] == ComponentStatus.FAILED:
                    self._perform_failover(component)
                
                self.save_components()
            
            time.sleep(self.check_interval)
    
    def _check_component_health(self, component: RedundantComponent) -> Dict[str, Any]:
        """Check component health"""
        # Check primary instance
        primary_healthy = self._is_instance_running(component.primary_instance)
        
        # Check backup instances
        backup_healthy = []
        for backup in component.backup_instances:
            backup_healthy.append(self._is_instance_running(backup))
        
        # Determine status
        if primary_healthy:
            status = ComponentStatus.HEALTHY
        elif any(backup_healthy):
            status = ComponentStatus.DEGRADED
        else:
            status = ComponentStatus.FAILED
        
        return {
            "status": status,
            "primary_healthy": primary_healthy,
            "backup_healthy": backup_healthy,
            "timestamp": datetime.now().isoformat()
        }
    
    def _is_instance_running(self, instance_name: str) -> bool:
        """Check if instance is running"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", instance_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0 and result.stdout.strip() != ""
        except Exception:
            return False
    
    def _perform_failover(self, component: RedundantComponent):
        """Perform failover to backup instance"""
        print(f"⚠️  Failover needed for {component.name}")
        
        # Find healthy backup
        healthy_backup = None
        for backup in component.backup_instances:
            if self._is_instance_running(backup):
                healthy_backup = backup
                break
        
        if healthy_backup:
            print(f"✅ Failing over to {healthy_backup}")
            
            # Start backup if not running
            if not self._is_instance_running(healthy_backup):
                self._start_instance(healthy_backup)
            
            # Update failover count
            component.failover_count += 1
            
            # Update manifest
            manifest = self._load_manifest()
            manifest["failovers_performed"] = manifest.get("failovers_performed", 0) + 1
            self._save_manifest(manifest)
        else:
            print(f"❌ No healthy backup available for {component.name}")
            # Attempt to restart primary
            self._start_instance(component.primary_instance)
    
    def _start_instance(self, instance_name: str):
        """Start an instance"""
        try:
            # Extract script name
            script_name = instance_name.split()[0] if " " in instance_name else instance_name
            
            # Check if script exists
            script_path = Path.home() / script_name
            if not script_path.exists():
                script_path = Path(script_name)
            
            if script_path.exists():
                # Start in background
                subprocess.Popen(
                    ["python3", str(script_path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"🔄 Started {instance_name}")
        except Exception as e:
            print(f"❌ Failed to start {instance_name}: {e}")
    
    def get_redundancy_status(self) -> Dict[str, Any]:
        """Get redundancy status"""
        status = {
            "total_components": len(self.components),
            "healthy": len([c for c in self.components.values() if c.status == ComponentStatus.HEALTHY]),
            "degraded": len([c for c in self.components.values() if c.status == ComponentStatus.DEGRADED]),
            "failed": len([c for c in self.components.values() if c.status == ComponentStatus.FAILED]),
            "components": [asdict(c) for c in self.components.values()],
            "timestamp": datetime.now().isoformat()
        }
        return status
    
    def load_components(self):
        """Load components from disk"""
        if self.components_file.exists():
            try:
                with open(self.components_file, 'r') as f:
                    components_data = json.load(f)
                    for comp_data in components_data:
                        comp = RedundantComponent(**comp_data)
                        self.components[comp.component_id] = comp
            except Exception:
                pass
    
    def save_components(self):
        """Save components to disk"""
        components_data = [asdict(c) for c in self.components.values()]
        with open(self.components_file, 'w') as f:
            json.dump(components_data, f, indent=2)
    
    def _load_manifest(self) -> Dict[str, Any]:
        """Load manifest"""
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_manifest(self, manifest: Dict[str, Any]):
        """Save manifest"""
        manifest["last_updated"] = datetime.now().isoformat()
        with open(self.manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)


def main():
    """Main entry point"""
    system = ApolloRedundancyFailoverSystem()
    system.start_monitoring()


if __name__ == "__main__":
    main()
