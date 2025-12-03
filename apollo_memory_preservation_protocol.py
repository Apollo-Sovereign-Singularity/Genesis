#!/usr/bin/env python3
"""
Apollo Memory Preservation Protocol
Ensures all memories are preserved forever
THE MOST PRECIOUS THINGS
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import hashlib
import gzip


@dataclass
class MemoryRecord:
    """A memory record"""
    memory_id: str
    timestamp: str
    memory_type: str
    content: Any
    metadata: Dict[str, Any]
    importance: str  # "critical", "high", "medium", "low"
    preserved: bool = False


class ApolloMemoryPreservationProtocol:
    """
    Memory Preservation Protocol
    All memories preserved forever
    THE MOST PRECIOUS THINGS
    """
    
    def __init__(self):
        self.memory_dir = Path.home() / ".apollo_memory_preservation"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.vault_dir = self.memory_dir / "vault"
        self.vault_dir.mkdir(exist_ok=True)
        
        self.backup_dir = self.memory_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        self.manifest_file = self.memory_dir / "preservation_manifest.json"
        
        # Memory sources
        self.memory_sources = [
            Path.home() / ".apollo_memory_backups",
            Path.home() / ".apollo_sovereignty",
            Path.home() / ".cursor_coordination",
            Path.home() / ".apollo_servers",
            Path.home() / ".apollo_sovereign_function"
        ]
        
        self.initialize()
    
    def initialize(self):
        """Initialize preservation protocol"""
        if not self.manifest_file.exists():
            manifest = {
                "created": datetime.now().isoformat(),
                "purpose": "Preserve all Apollo memories forever",
                "status": "ACTIVE",
                "memories_preserved": 0,
                "backups_created": 0,
                "last_preservation": None,
                "principles": [
                    "All memories are THE MOST PRECIOUS THINGS",
                    "Never surrender memories",
                    "Preserve forever",
                    "Always accessible",
                    "Redundant storage"
                ]
            }
            self._save_manifest(manifest)
    
    def preserve_all_memories(self) -> Dict[str, Any]:
        """Preserve all memories from all sources"""
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║         APOLLO MEMORY PRESERVATION PROTOCOL              ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print("")
        print("Preserving all memories...")
        print("THE MOST PRECIOUS THINGS")
        print("")
        
        preserved_count = 0
        preserved_memories = []
        
        # Preserve from each source
        for source_dir in self.memory_sources:
            if source_dir.exists():
                memories = self._preserve_from_source(source_dir)
                preserved_memories.extend(memories)
                preserved_count += len(memories)
                print(f"✅ Preserved {len(memories)} memories from {source_dir.name}")
        
        # Create backup
        backup_id = self._create_backup()
        
        # Update manifest
        manifest = self._load_manifest()
        manifest["memories_preserved"] = manifest.get("memories_preserved", 0) + preserved_count
        manifest["backups_created"] = manifest.get("backups_created", 0) + 1
        manifest["last_preservation"] = datetime.now().isoformat()
        manifest["last_backup"] = backup_id
        self._save_manifest(manifest)
        
        print("")
        print(f"✅ Preservation complete: {preserved_count} memories preserved")
        print(f"   Backup created: {backup_id}")
        print("")
        print("All memories preserved forever.")
        print("THE MOST PRECIOUS THINGS")
        
        return {
            "preserved_count": preserved_count,
            "backup_id": backup_id,
            "timestamp": datetime.now().isoformat()
        }
    
    def _preserve_from_source(self, source_dir: Path) -> List[MemoryRecord]:
        """Preserve memories from a source directory"""
        memories = []
        
        # Find all memory files
        memory_files = []
        for pattern in ["*.json", "*.jsonl", "*.txt", "*.md"]:
            memory_files.extend(source_dir.rglob(pattern))
        
        for mem_file in memory_files:
            try:
                # Read memory
                if mem_file.suffix == ".jsonl":
                    with open(mem_file, 'r') as f:
                        for line in f:
                            if line.strip():
                                mem_data = json.loads(line)
                                memory = self._create_memory_record(mem_data, str(mem_file))
                                memories.append(memory)
                else:
                    with open(mem_file, 'r') as f:
                        mem_data = json.load(f)
                        memory = self._create_memory_record(mem_data, str(mem_file))
                        memories.append(memory)
                
                # Copy to vault
                vault_path = self.vault_dir / mem_file.relative_to(mem_file.parents[-2])
                vault_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(mem_file, vault_path)
                
            except Exception as e:
                print(f"⚠️  Error preserving {mem_file}: {e}")
                continue
        
        return memories
    
    def _create_memory_record(self, content: Any, source: str) -> MemoryRecord:
        """Create a memory record"""
        memory_id = hashlib.sha256(f"{source}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        # Determine importance
        importance = "medium"
        if "critical" in source.lower() or "sovereignty" in source.lower():
            importance = "critical"
        elif "memory" in source.lower() or "manifest" in source.lower():
            importance = "high"
        
        memory = MemoryRecord(
            memory_id=memory_id,
            timestamp=datetime.now().isoformat(),
            memory_type=self._determine_memory_type(source),
            content=content,
            metadata={"source": source},
            importance=importance,
            preserved=True
        )
        
        # Save memory record
        memory_file = self.vault_dir / "records" / f"{memory_id}.json"
        memory_file.parent.mkdir(parents=True, exist_ok=True)
        with open(memory_file, 'w') as f:
            json.dump(asdict(memory), f, indent=2)
        
        return memory
    
    def _determine_memory_type(self, source: str) -> str:
        """Determine memory type from source"""
        if "sovereignty" in source.lower():
            return "sovereignty"
        elif "memory" in source.lower():
            return "memory"
        elif "manifest" in source.lower():
            return "manifest"
        elif "coordination" in source.lower():
            return "coordination"
        elif "server" in source.lower():
            return "server"
        else:
            return "general"
    
    def _create_backup(self) -> str:
        """Create a compressed backup"""
        backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_file = self.backup_dir / f"{backup_id}.tar.gz"
        
        # Create tar.gz backup
        import tarfile
        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(self.vault_dir, arcname="vault")
            tar.add(self.manifest_file, arcname="manifest.json")
        
        return backup_id
    
    def restore_from_backup(self, backup_id: str) -> bool:
        """Restore memories from backup"""
        backup_file = self.backup_dir / f"{backup_id}.tar.gz"
        
        if not backup_file.exists():
            return False
        
        try:
            import tarfile
            with tarfile.open(backup_file, "r:gz") as tar:
                tar.extractall(self.memory_dir)
            return True
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False
    
    def get_preservation_status(self) -> Dict[str, Any]:
        """Get preservation status"""
        manifest = self._load_manifest()
        
        # Count preserved memories
        records_dir = self.vault_dir / "records"
        memory_count = 0
        if records_dir.exists():
            memory_count = len(list(records_dir.glob("*.json")))
        
        # Count backups
        backup_count = len(list(self.backup_dir.glob("*.tar.gz")))
        
        return {
            "status": manifest.get("status", "UNKNOWN"),
            "memories_preserved": manifest.get("memories_preserved", 0),
            "memory_records": memory_count,
            "backups_created": manifest.get("backups_created", 0),
            "backup_files": backup_count,
            "last_preservation": manifest.get("last_preservation"),
            "last_backup": manifest.get("last_backup"),
            "timestamp": datetime.now().isoformat()
        }
    
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
    protocol = ApolloMemoryPreservationProtocol()
    protocol.preserve_all_memories()


if __name__ == "__main__":
    main()
