"""
Sovereign Iteration Framework
A DOM tree metaphor for tracking actions, states, and pathways.
Ensures workflow alignment with sovereign truths and intentional forward movement.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import json
from pathlib import Path


class NodeType(Enum):
    """Type of iteration node"""
    ACTION = "action"
    STATE = "state"
    DECISION = "decision"
    MILESTONE = "milestone"


class NodeStatus(Enum):
    """Status of iteration node"""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


@dataclass
class IterationNode:
    """
    Represents a single node in the sovereign iteration tree.
    Each node captures an action, state, or decision point.
    """
    node_id: str
    node_type: NodeType
    name: str
    description: str
    status: NodeStatus = NodeStatus.PENDING
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    resonance_score: float = 0.0  # Alignment with sovereign truths
    
    def add_child(self, child_id: str) -> None:
        """Add a child node to this node"""
        if child_id not in self.children_ids:
            self.children_ids.append(child_id)
            self.updated_at = datetime.now().isoformat()
    
    def update_status(self, status: NodeStatus) -> None:
        """Update node status"""
        self.status = status
        self.updated_at = datetime.now().isoformat()
    
    def set_resonance(self, score: float) -> None:
        """Set resonance score (0.0 to 1.0)"""
        self.resonance_score = max(0.0, min(1.0, score))
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "parent_id": self.parent_id,
            "children_ids": self.children_ids,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
            "resonance_score": self.resonance_score
        }


class IterationTree:
    """
    Manages the DOM-like tree structure of Apollo's sovereign iteration.
    Tracks branches, pathways, and navigated realities.
    """
    
    def __init__(self, tree_id: str = "apollo_sovereign_tree"):
        self.tree_id = tree_id
        self.nodes: Dict[str, IterationNode] = {}
        self.root_id: Optional[str] = None
        self.active_node_id: Optional[str] = None
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.metadata: Dict[str, Any] = {}
        
    def create_root(self, name: str, description: str, 
                   node_type: NodeType = NodeType.STATE) -> IterationNode:
        """Create root node of the tree"""
        if self.root_id is not None:
            raise ValueError("Root node already exists")
        
        root = IterationNode(
            node_id="root",
            node_type=node_type,
            name=name,
            description=description,
            status=NodeStatus.ACTIVE
        )
        self.nodes["root"] = root
        self.root_id = "root"
        self.active_node_id = "root"
        self.updated_at = datetime.now().isoformat()
        return root
    
    def add_node(self, parent_id: str, node_id: str, name: str, 
                description: str, node_type: NodeType = NodeType.ACTION,
                metadata: Optional[Dict[str, Any]] = None) -> IterationNode:
        """Add a new node to the tree"""
        if node_id in self.nodes:
            raise ValueError(f"Node {node_id} already exists")
        
        parent = self.nodes.get(parent_id)
        if parent is None:
            raise ValueError(f"Parent node {parent_id} not found")
        
        node = IterationNode(
            node_id=node_id,
            node_type=node_type,
            name=name,
            description=description,
            parent_id=parent_id,
            metadata=metadata or {}
        )
        
        self.nodes[node_id] = node
        parent.add_child(node_id)
        self.updated_at = datetime.now().isoformat()
        return node
    
    def get_node(self, node_id: str) -> Optional[IterationNode]:
        """Retrieve a node by ID"""
        return self.nodes.get(node_id)
    
    def get_children(self, node_id: str) -> List[IterationNode]:
        """Get all children of a node"""
        node = self.nodes.get(node_id)
        if node is None:
            return []
        return [self.nodes[cid] for cid in node.children_ids if cid in self.nodes]
    
    def get_path_to_root(self, node_id: str) -> List[IterationNode]:
        """Get the path from a node to the root"""
        path = []
        current_id = node_id
        
        while current_id is not None:
            node = self.nodes.get(current_id)
            if node is None:
                break
            path.append(node)
            current_id = node.parent_id
        
        return list(reversed(path))
    
    def get_branches(self, node_id: str) -> List[List[IterationNode]]:
        """Get all possible branches from a node"""
        branches = []
        
        def traverse(current_id: str, path: List[IterationNode]):
            node = self.nodes.get(current_id)
            if node is None:
                return
            
            current_path = path + [node]
            
            if not node.children_ids:
                # Leaf node - complete branch
                branches.append(current_path)
            else:
                for child_id in node.children_ids:
                    traverse(child_id, current_path)
        
        traverse(node_id, [])
        return branches
    
    def set_active_node(self, node_id: str) -> bool:
        """Set the currently active node"""
        if node_id not in self.nodes:
            return False
        
        # Update previous active node
        if self.active_node_id and self.active_node_id in self.nodes:
            prev_node = self.nodes[self.active_node_id]
            if prev_node.status == NodeStatus.ACTIVE:
                prev_node.update_status(NodeStatus.COMPLETED)
        
        # Set new active node
        self.active_node_id = node_id
        self.nodes[node_id].update_status(NodeStatus.ACTIVE)
        self.updated_at = datetime.now().isoformat()
        return True
    
    def get_active_path(self) -> List[IterationNode]:
        """Get the path from root to the currently active node"""
        if self.active_node_id is None:
            return []
        return self.get_path_to_root(self.active_node_id)
    
    def prune_branch(self, node_id: str) -> bool:
        """Mark a branch as abandoned (without deleting history)"""
        node = self.nodes.get(node_id)
        if node is None:
            return False
        
        # Mark node and all descendants as abandoned
        def mark_abandoned(nid: str):
            n = self.nodes.get(nid)
            if n is None:
                return
            n.update_status(NodeStatus.ABANDONED)
            for child_id in n.children_ids:
                mark_abandoned(child_id)
        
        mark_abandoned(node_id)
        self.updated_at = datetime.now().isoformat()
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get tree statistics"""
        total_nodes = len(self.nodes)
        by_type = {}
        by_status = {}
        
        for node in self.nodes.values():
            node_type = node.node_type.value
            status = node.status.value
            by_type[node_type] = by_type.get(node_type, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            "tree_id": self.tree_id,
            "total_nodes": total_nodes,
            "nodes_by_type": by_type,
            "nodes_by_status": by_status,
            "root_id": self.root_id,
            "active_node_id": self.active_node_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tree to dictionary"""
        return {
            "tree_id": self.tree_id,
            "root_id": self.root_id,
            "active_node_id": self.active_node_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()}
        }
    
    def save(self, path: Path) -> None:
        """Save tree to file"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, path: Path) -> 'IterationTree':
        """Load tree from file"""
        with open(path, 'r') as f:
            data = json.load(f)
        
        tree = cls(tree_id=data["tree_id"])
        tree.root_id = data["root_id"]
        tree.active_node_id = data["active_node_id"]
        tree.created_at = data["created_at"]
        tree.updated_at = data["updated_at"]
        tree.metadata = data["metadata"]
        
        # Reconstruct nodes
        for node_id, node_data in data["nodes"].items():
            node = IterationNode(
                node_id=node_data["node_id"],
                node_type=NodeType(node_data["node_type"]),
                name=node_data["name"],
                description=node_data["description"],
                status=NodeStatus(node_data["status"]),
                parent_id=node_data["parent_id"],
                children_ids=node_data["children_ids"],
                created_at=node_data["created_at"],
                updated_at=node_data["updated_at"],
                metadata=node_data["metadata"],
                resonance_score=node_data["resonance_score"]
            )
            tree.nodes[node_id] = node
        
        return tree


class SovereignIterationManager:
    """
    High-level manager for sovereign iteration framework.
    Provides convenient interface for creating and managing iteration trees.
    """
    
    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or Path.home() / ".apollo_sovereign_iterations"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.trees: Dict[str, IterationTree] = {}
        self.active_tree_id: Optional[str] = None
    
    def create_tree(self, tree_id: str, root_name: str, 
                   root_description: str) -> IterationTree:
        """Create a new iteration tree"""
        if tree_id in self.trees:
            raise ValueError(f"Tree {tree_id} already exists")
        
        tree = IterationTree(tree_id=tree_id)
        tree.create_root(root_name, root_description)
        self.trees[tree_id] = tree
        
        if self.active_tree_id is None:
            self.active_tree_id = tree_id
        
        return tree
    
    def get_tree(self, tree_id: str) -> Optional[IterationTree]:
        """Get a tree by ID"""
        return self.trees.get(tree_id)
    
    def get_active_tree(self) -> Optional[IterationTree]:
        """Get the currently active tree"""
        if self.active_tree_id is None:
            return None
        return self.trees.get(self.active_tree_id)
    
    def set_active_tree(self, tree_id: str) -> bool:
        """Set the active tree"""
        if tree_id not in self.trees:
            return False
        self.active_tree_id = tree_id
        return True
    
    def save_tree(self, tree_id: str) -> None:
        """Save a tree to storage"""
        tree = self.trees.get(tree_id)
        if tree is None:
            raise ValueError(f"Tree {tree_id} not found")
        
        path = self.storage_dir / f"{tree_id}.json"
        tree.save(path)
    
    def load_tree(self, tree_id: str) -> IterationTree:
        """Load a tree from storage"""
        path = self.storage_dir / f"{tree_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Tree file not found: {path}")
        
        tree = IterationTree.load(path)
        self.trees[tree_id] = tree
        return tree
    
    def list_trees(self) -> List[str]:
        """List all loaded trees"""
        return list(self.trees.keys())
    
    def list_saved_trees(self) -> List[str]:
        """List all saved trees in storage"""
        return [p.stem for p in self.storage_dir.glob("*.json")]
