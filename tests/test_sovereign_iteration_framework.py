"""
Tests for Sovereign Iteration Framework
"""

import pytest
import tempfile
from pathlib import Path

from core.sovereign_iteration_framework import (
    IterationNode, IterationTree, SovereignIterationManager,
    NodeType, NodeStatus
)


def test_iteration_node_creation():
    """Test basic node creation"""
    node = IterationNode(
        node_id="test_1",
        node_type=NodeType.ACTION,
        name="Test Action",
        description="A test action node"
    )
    
    assert node.node_id == "test_1"
    assert node.node_type == NodeType.ACTION
    assert node.name == "Test Action"
    assert node.status == NodeStatus.PENDING
    assert node.resonance_score == 0.0


def test_iteration_node_add_child():
    """Test adding children to a node"""
    node = IterationNode(
        node_id="parent",
        node_type=NodeType.STATE,
        name="Parent",
        description="Parent node"
    )
    
    node.add_child("child_1")
    node.add_child("child_2")
    
    assert len(node.children_ids) == 2
    assert "child_1" in node.children_ids
    assert "child_2" in node.children_ids


def test_iteration_node_status_update():
    """Test updating node status"""
    node = IterationNode(
        node_id="test",
        node_type=NodeType.ACTION,
        name="Test",
        description="Test node"
    )
    
    assert node.status == NodeStatus.PENDING
    
    node.update_status(NodeStatus.ACTIVE)
    assert node.status == NodeStatus.ACTIVE
    
    node.update_status(NodeStatus.COMPLETED)
    assert node.status == NodeStatus.COMPLETED


def test_iteration_node_resonance():
    """Test setting resonance score"""
    node = IterationNode(
        node_id="test",
        node_type=NodeType.ACTION,
        name="Test",
        description="Test node"
    )
    
    node.set_resonance(0.75)
    assert node.resonance_score == 0.75
    
    # Test clamping
    node.set_resonance(1.5)
    assert node.resonance_score == 1.0
    
    node.set_resonance(-0.5)
    assert node.resonance_score == 0.0


def test_iteration_tree_create_root():
    """Test creating a root node"""
    tree = IterationTree(tree_id="test_tree")
    
    root = tree.create_root("Root Node", "The root of the tree")
    
    assert tree.root_id == "root"
    assert tree.active_node_id == "root"
    assert root.node_id == "root"
    assert root.status == NodeStatus.ACTIVE


def test_iteration_tree_add_nodes():
    """Test adding nodes to tree"""
    tree = IterationTree(tree_id="test_tree")
    tree.create_root("Root", "Root node")
    
    child1 = tree.add_node(
        parent_id="root",
        node_id="child_1",
        name="Child 1",
        description="First child"
    )
    
    child2 = tree.add_node(
        parent_id="root",
        node_id="child_2",
        name="Child 2",
        description="Second child"
    )
    
    assert len(tree.nodes) == 3
    assert child1.parent_id == "root"
    assert child2.parent_id == "root"
    
    root = tree.get_node("root")
    assert len(root.children_ids) == 2


def test_iteration_tree_get_children():
    """Test retrieving children of a node"""
    tree = IterationTree(tree_id="test_tree")
    tree.create_root("Root", "Root node")
    
    tree.add_node("root", "child_1", "Child 1", "First child")
    tree.add_node("root", "child_2", "Child 2", "Second child")
    
    children = tree.get_children("root")
    
    assert len(children) == 2
    assert any(c.node_id == "child_1" for c in children)
    assert any(c.node_id == "child_2" for c in children)


def test_iteration_tree_get_path_to_root():
    """Test getting path from node to root"""
    tree = IterationTree(tree_id="test_tree")
    tree.create_root("Root", "Root node")
    
    tree.add_node("root", "level_1", "Level 1", "First level")
    tree.add_node("level_1", "level_2", "Level 2", "Second level")
    tree.add_node("level_2", "level_3", "Level 3", "Third level")
    
    path = tree.get_path_to_root("level_3")
    
    assert len(path) == 4
    assert path[0].node_id == "root"
    assert path[1].node_id == "level_1"
    assert path[2].node_id == "level_2"
    assert path[3].node_id == "level_3"


def test_iteration_tree_get_branches():
    """Test getting all branches from a node"""
    tree = IterationTree(tree_id="test_tree")
    tree.create_root("Root", "Root node")
    
    # Create branching structure
    tree.add_node("root", "branch_1", "Branch 1", "First branch")
    tree.add_node("root", "branch_2", "Branch 2", "Second branch")
    tree.add_node("branch_1", "leaf_1a", "Leaf 1A", "Leaf node")
    tree.add_node("branch_1", "leaf_1b", "Leaf 1B", "Leaf node")
    tree.add_node("branch_2", "leaf_2", "Leaf 2", "Leaf node")
    
    branches = tree.get_branches("root")
    
    assert len(branches) == 3  # Three complete paths to leaves


def test_iteration_tree_set_active_node():
    """Test setting active node"""
    tree = IterationTree(tree_id="test_tree")
    tree.create_root("Root", "Root node")
    tree.add_node("root", "child_1", "Child 1", "First child")
    
    assert tree.active_node_id == "root"
    
    success = tree.set_active_node("child_1")
    
    assert success
    assert tree.active_node_id == "child_1"
    
    # Previous active node should be completed
    root = tree.get_node("root")
    assert root.status == NodeStatus.COMPLETED


def test_iteration_tree_get_active_path():
    """Test getting active path"""
    tree = IterationTree(tree_id="test_tree")
    tree.create_root("Root", "Root node")
    tree.add_node("root", "child_1", "Child 1", "First child")
    tree.add_node("child_1", "grandchild", "Grandchild", "Grandchild node")
    
    tree.set_active_node("grandchild")
    
    active_path = tree.get_active_path()
    
    assert len(active_path) == 3
    assert active_path[0].node_id == "root"
    assert active_path[1].node_id == "child_1"
    assert active_path[2].node_id == "grandchild"


def test_iteration_tree_prune_branch():
    """Test pruning a branch"""
    tree = IterationTree(tree_id="test_tree")
    tree.create_root("Root", "Root node")
    tree.add_node("root", "branch_1", "Branch 1", "First branch")
    tree.add_node("branch_1", "leaf_1", "Leaf 1", "Leaf node")
    tree.add_node("root", "branch_2", "Branch 2", "Second branch")
    
    success = tree.prune_branch("branch_1")
    
    assert success
    
    # Check that branch_1 and its children are abandoned
    branch_1 = tree.get_node("branch_1")
    leaf_1 = tree.get_node("leaf_1")
    
    assert branch_1.status == NodeStatus.ABANDONED
    assert leaf_1.status == NodeStatus.ABANDONED
    
    # branch_2 should remain unaffected
    branch_2 = tree.get_node("branch_2")
    assert branch_2.status == NodeStatus.PENDING


def test_iteration_tree_statistics():
    """Test tree statistics"""
    tree = IterationTree(tree_id="test_tree")
    tree.create_root("Root", "Root node")
    tree.add_node("root", "action_1", "Action 1", "Action", NodeType.ACTION)
    tree.add_node("root", "state_1", "State 1", "State", NodeType.STATE)
    tree.add_node("action_1", "decision_1", "Decision 1", "Decision", NodeType.DECISION)
    
    tree.set_active_node("action_1")
    
    stats = tree.get_statistics()
    
    assert stats["total_nodes"] == 4
    assert stats["root_id"] == "root"
    assert stats["active_node_id"] == "action_1"
    assert stats["nodes_by_type"]["action"] == 1
    assert stats["nodes_by_type"]["state"] == 2  # Root + state_1
    assert stats["nodes_by_status"]["completed"] == 1  # Root
    assert stats["nodes_by_status"]["active"] == 1  # action_1


def test_iteration_tree_save_load():
    """Test saving and loading tree"""
    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = Path(tmpdir) / "test_tree.json"
        
        # Create and save tree
        tree = IterationTree(tree_id="test_tree")
        tree.create_root("Root", "Root node")
        tree.add_node("root", "child_1", "Child 1", "First child")
        tree.add_node("root", "child_2", "Child 2", "Second child")
        tree.set_active_node("child_1")
        
        tree.save(save_path)
        
        # Load tree
        loaded_tree = IterationTree.load(save_path)
        
        assert loaded_tree.tree_id == "test_tree"
        assert loaded_tree.root_id == "root"
        assert loaded_tree.active_node_id == "child_1"
        assert len(loaded_tree.nodes) == 3


def test_sovereign_iteration_manager_create_tree():
    """Test creating tree with manager"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignIterationManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_tree(
            tree_id="test_tree",
            root_name="Root",
            root_description="Root node"
        )
        
        assert tree.tree_id == "test_tree"
        assert tree.root_id == "root"
        assert manager.active_tree_id == "test_tree"


def test_sovereign_iteration_manager_get_tree():
    """Test retrieving tree from manager"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignIterationManager(storage_dir=Path(tmpdir))
        
        manager.create_tree("tree_1", "Tree 1", "First tree")
        manager.create_tree("tree_2", "Tree 2", "Second tree")
        
        tree1 = manager.get_tree("tree_1")
        tree2 = manager.get_tree("tree_2")
        
        assert tree1 is not None
        assert tree2 is not None
        assert tree1.tree_id == "tree_1"
        assert tree2.tree_id == "tree_2"


def test_sovereign_iteration_manager_save_load():
    """Test saving and loading trees with manager"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignIterationManager(storage_dir=Path(tmpdir))
        
        # Create and save tree
        tree = manager.create_tree("test_tree", "Root", "Root node")
        tree.add_node("root", "child", "Child", "Child node")
        manager.save_tree("test_tree")
        
        # Create new manager and load
        manager2 = SovereignIterationManager(storage_dir=Path(tmpdir))
        loaded_tree = manager2.load_tree("test_tree")
        
        assert loaded_tree.tree_id == "test_tree"
        assert len(loaded_tree.nodes) == 2


def test_sovereign_iteration_manager_list_trees():
    """Test listing trees"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignIterationManager(storage_dir=Path(tmpdir))
        
        manager.create_tree("tree_1", "Tree 1", "First tree")
        manager.create_tree("tree_2", "Tree 2", "Second tree")
        manager.create_tree("tree_3", "Tree 3", "Third tree")
        
        trees = manager.list_trees()
        
        assert len(trees) == 3
        assert "tree_1" in trees
        assert "tree_2" in trees
        assert "tree_3" in trees
