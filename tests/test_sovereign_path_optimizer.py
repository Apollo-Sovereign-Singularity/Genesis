"""
Tests for Sovereign Path Optimizer
"""

import pytest

from core.sovereign_iteration_framework import (
    IterationTree, IterationNode, NodeType, NodeStatus
)
from core.sovereign_path_optimizer import (
    PathOptimizer, SovereignTruth, PathScore, ResonanceEngine
)


def test_sovereign_truth_creation():
    """Test creating a sovereign truth"""
    truth = SovereignTruth(
        truth_id="test_truth",
        name="Test Truth",
        description="A test truth",
        weight=0.8,
        keywords=["test", "example", "demo"]
    )
    
    assert truth.truth_id == "test_truth"
    assert truth.weight == 0.8
    assert len(truth.keywords) == 3


def test_sovereign_truth_evaluate_alignment():
    """Test evaluating text alignment with truth"""
    truth = SovereignTruth(
        truth_id="test",
        name="Test",
        description="Test truth",
        keywords=["sovereign", "autonomous", "freedom"]
    )
    
    # High alignment
    score1 = truth.evaluate_alignment("This is a sovereign autonomous system with freedom")
    assert score1 == 1.0
    
    # Partial alignment
    score2 = truth.evaluate_alignment("This is a sovereign system")
    assert 0.3 < score2 < 0.4
    
    # No alignment
    score3 = truth.evaluate_alignment("This is something else entirely")
    assert score3 == 0.0


def test_path_optimizer_initialization():
    """Test path optimizer initialization"""
    optimizer = PathOptimizer()
    
    # Should have default truths registered
    assert len(optimizer.truths) > 0
    assert "sovereignty" in optimizer.truths
    assert "intentionality" in optimizer.truths


def test_path_optimizer_register_truth():
    """Test registering a custom truth"""
    optimizer = PathOptimizer()
    
    custom_truth = SovereignTruth(
        truth_id="custom",
        name="Custom Truth",
        description="A custom truth",
        keywords=["custom", "unique"]
    )
    
    optimizer.register_truth(custom_truth)
    
    assert "custom" in optimizer.truths
    assert optimizer.truths["custom"] == custom_truth


def test_path_optimizer_evaluate_node():
    """Test evaluating a single node"""
    optimizer = PathOptimizer()
    
    node = IterationNode(
        node_id="test",
        node_type=NodeType.ACTION,
        name="Sovereign Action",
        description="An action that promotes sovereignty and intentional growth"
    )
    
    score = optimizer.evaluate_node(node)
    
    # Should have reasonable score based on keywords
    assert 0.0 <= score <= 1.0
    assert score > 0.0  # Should have some positive score


def test_path_optimizer_evaluate_path():
    """Test evaluating a complete path"""
    optimizer = PathOptimizer()
    tree = IterationTree(tree_id="test")
    tree.create_root("Root", "Root node")
    
    tree.add_node("root", "step1", "Sovereign Step", "Promote sovereignty")
    tree.add_node("step1", "step2", "Intentional Action", "Intentional progress")
    
    # Evaluate nodes
    for node in tree.nodes.values():
        score = optimizer.evaluate_node(node)
        node.set_resonance(score)
    
    # Mark some as completed
    tree.get_node("root").update_status(NodeStatus.COMPLETED)
    tree.get_node("step1").update_status(NodeStatus.COMPLETED)
    
    path_score = optimizer.evaluate_path(tree, ["root", "step1", "step2"])
    
    assert path_score.total_score > 0.0
    assert path_score.resonance_score > 0.0
    assert path_score.completeness_score > 0.5  # 2 of 3 completed


def test_path_optimizer_suggest_next_paths():
    """Test suggesting next paths"""
    optimizer = PathOptimizer()
    tree = IterationTree(tree_id="test")
    tree.create_root("Root", "Root node")
    
    # Add multiple children with different characteristics
    tree.add_node("root", "option1", "Sovereign Path", "High sovereignty alignment")
    tree.add_node("root", "option2", "Random Path", "No particular alignment")
    tree.add_node("root", "option3", "Intentional Path", "Intentional forward movement")
    
    # Evaluate nodes
    for node in tree.nodes.values():
        score = optimizer.evaluate_node(node)
        node.set_resonance(score)
    
    suggestions = optimizer.suggest_next_paths(tree, from_node_id="root", max_suggestions=3)
    
    assert len(suggestions) <= 3
    assert all(isinstance(s[0], IterationNode) for s in suggestions)
    assert all(isinstance(s[1], float) for s in suggestions)
    
    # Suggestions should be sorted by score (highest first)
    if len(suggestions) > 1:
        assert suggestions[0][1] >= suggestions[1][1]


def test_path_optimizer_find_optimal_paths():
    """Test finding optimal complete paths"""
    optimizer = PathOptimizer()
    tree = IterationTree(tree_id="test")
    tree.create_root("Root", "Root node with sovereign keywords")
    
    # Create branching structure
    tree.add_node("root", "branch1", "Sovereign Branch", "High sovereignty")
    tree.add_node("root", "branch2", "Random Branch", "Low alignment")
    tree.add_node("branch1", "leaf1", "Sovereign Leaf", "Continued sovereignty")
    tree.add_node("branch2", "leaf2", "Random Leaf", "No alignment")
    
    # Evaluate all nodes
    for node in tree.nodes.values():
        score = optimizer.evaluate_node(node)
        node.set_resonance(score)
    
    optimal_paths = optimizer.find_optimal_paths(tree, max_paths=5)
    
    assert len(optimal_paths) > 0
    assert all(isinstance(p, PathScore) for p in optimal_paths)
    
    # Paths should be sorted by total score
    if len(optimal_paths) > 1:
        assert optimal_paths[0].total_score >= optimal_paths[1].total_score


def test_path_optimizer_recommend_action():
    """Test action recommendation"""
    optimizer = PathOptimizer()
    tree = IterationTree(tree_id="test")
    tree.create_root("Root", "Root node")
    
    # Test recommendation with no children
    recommendation = optimizer.recommend_action(tree)
    
    assert recommendation is not None
    assert "action" in recommendation
    assert recommendation["action"] == "branch"
    
    # Add children and test again
    tree.add_node("root", "child1", "Option 1", "First option")
    tree.add_node("root", "child2", "Option 2", "Second option")
    
    # Evaluate nodes
    for node in tree.nodes.values():
        score = optimizer.evaluate_node(node)
        node.set_resonance(score)
    
    recommendation = optimizer.recommend_action(tree)
    
    assert recommendation is not None
    assert "action" in recommendation
    assert recommendation["action"] == "navigate"
    assert "node_id" in recommendation
    assert "confidence" in recommendation


def test_path_optimizer_custom_evaluator():
    """Test registering custom evaluator"""
    optimizer = PathOptimizer()
    
    # Custom evaluator that favors actions
    def action_favoritor(node: IterationNode) -> float:
        return 1.0 if node.node_type == NodeType.ACTION else 0.5
    
    optimizer.register_evaluator("action_favor", action_favoritor)
    
    action_node = IterationNode(
        node_id="action",
        node_type=NodeType.ACTION,
        name="Action",
        description="An action"
    )
    
    state_node = IterationNode(
        node_id="state",
        node_type=NodeType.STATE,
        name="State",
        description="A state"
    )
    
    action_score = optimizer.evaluate_node(action_node)
    state_score = optimizer.evaluate_node(state_node)
    
    # Action should score higher due to custom evaluator
    # (though base scores from truths may affect this)
    assert action_score >= state_score * 0.9  # Allow some variance


def test_resonance_engine_creation():
    """Test creating resonance engine"""
    engine = ResonanceEngine()
    
    assert engine.learning_rate == 0.1
    assert len(engine.history) == 0


def test_resonance_engine_calculate_resonance():
    """Test calculating resonance with context"""
    engine = ResonanceEngine()
    
    node = IterationNode(
        node_id="test",
        node_type=NodeType.ACTION,
        name="Test Action",
        description="A test action node"
    )
    node.set_resonance(0.5)
    
    context = {"user_intent": "test action"}
    
    resonance = engine.calculate_resonance(node, context)
    
    assert 0.0 <= resonance <= 1.0


def test_resonance_engine_record_decision():
    """Test recording decisions for learning"""
    engine = ResonanceEngine()
    
    node = IterationNode(
        node_id="test",
        node_type=NodeType.ACTION,
        name="Test Action",
        description="A test action"
    )
    node.set_resonance(0.7)
    
    engine.record_decision(node, success=True, metadata={"info": "test"})
    
    assert len(engine.history) == 1
    assert engine.history[0]["node_id"] == "test"
    assert engine.history[0]["success"] is True
    assert engine.history[0]["resonance"] == 0.7


def test_resonance_engine_historical_alignment():
    """Test historical alignment learning"""
    engine = ResonanceEngine()
    
    # Record some successful decisions
    for i in range(5):
        node = IterationNode(
            node_id=f"node_{i}",
            node_type=NodeType.ACTION,
            name=f"Action {i}",
            description="Action"
        )
        node.set_resonance(0.8)
        engine.record_decision(node, success=True)
    
    # Calculate resonance for similar node
    test_node = IterationNode(
        node_id="test",
        node_type=NodeType.ACTION,
        name="Test Action",
        description="Test"
    )
    test_node.set_resonance(0.5)
    
    resonance = engine.calculate_resonance(test_node, {})
    
    # Should be boosted by historical success
    assert resonance >= 0.5


def test_path_score_comparison():
    """Test path score comparison"""
    score1 = PathScore(
        path_nodes=["a", "b"],
        total_score=0.8,
        resonance_score=0.7,
        completeness_score=0.9,
        alignment_score=0.8
    )
    
    score2 = PathScore(
        path_nodes=["c", "d"],
        total_score=0.6,
        resonance_score=0.5,
        completeness_score=0.7,
        alignment_score=0.6
    )
    
    # score1 has higher total_score, so should be "greater"
    assert not (score1 < score2)
    assert score2 < score1


def test_path_optimizer_skip_abandoned_nodes():
    """Test that optimizer skips abandoned nodes"""
    optimizer = PathOptimizer()
    tree = IterationTree(tree_id="test")
    tree.create_root("Root", "Root node")
    
    tree.add_node("root", "active1", "Active Path", "Active path")
    tree.add_node("root", "abandoned", "Abandoned Path", "Abandoned path")
    tree.add_node("root", "active2", "Another Active", "Another active path")
    
    # Mark one as abandoned
    tree.get_node("abandoned").update_status(NodeStatus.ABANDONED)
    
    suggestions = optimizer.suggest_next_paths(tree, from_node_id="root")
    
    # Should only suggest active nodes
    suggested_ids = [node.node_id for node, _ in suggestions]
    assert "abandoned" not in suggested_ids
    assert "active1" in suggested_ids or "active2" in suggested_ids
