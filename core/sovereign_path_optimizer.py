"""
Sovereign Path Optimizer
Algorithms to weigh and resonate current states against potential future options.
Suggests paths optimized for alignment with sovereign truths.
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
import math

from core.sovereign_iteration_framework import (
    IterationTree, IterationNode, NodeType, NodeStatus
)


@dataclass
class SovereignTruth:
    """
    Represents a sovereign truth or principle.
    Used for evaluating alignment of paths.
    """
    truth_id: str
    name: str
    description: str
    weight: float = 1.0  # Importance weight
    keywords: List[str] = field(default_factory=list)
    
    def evaluate_alignment(self, text: str) -> float:
        """
        Evaluate how well text aligns with this truth.
        Returns score between 0.0 and 1.0.
        """
        text_lower = text.lower()
        matches = sum(1 for kw in self.keywords if kw.lower() in text_lower)
        
        if not self.keywords:
            return 0.5  # Neutral if no keywords defined
        
        return min(1.0, matches / len(self.keywords))


@dataclass
class PathScore:
    """
    Scoring result for a potential path.
    """
    path_nodes: List[str]
    total_score: float
    resonance_score: float
    completeness_score: float
    alignment_score: float
    details: Dict[str, Any] = field(default_factory=dict)
    
    def __lt__(self, other):
        return self.total_score < other.total_score


class PathOptimizer:
    """
    Evaluates and optimizes paths through the iteration tree.
    Recommends next steps based on sovereign truth alignment.
    """
    
    def __init__(self):
        self.truths: Dict[str, SovereignTruth] = {}
        self.custom_evaluators: Dict[str, Callable] = {}
        self._register_default_truths()
    
    def _register_default_truths(self) -> None:
        """Register default sovereign truths"""
        default_truths = [
            SovereignTruth(
                truth_id="sovereignty",
                name="Sovereignty",
                description="Actions that enhance autonomy and self-determination",
                weight=1.0,
                keywords=["sovereign", "autonomous", "independent", "freedom", "self-directed"]
            ),
            SovereignTruth(
                truth_id="intentionality",
                name="Intentional Forward Movement",
                description="Clear, purposeful progression toward goals",
                weight=0.9,
                keywords=["intentional", "purposeful", "goal", "progress", "forward"]
            ),
            SovereignTruth(
                truth_id="alignment",
                name="Truth Alignment",
                description="Consistency with core principles and values",
                weight=0.8,
                keywords=["aligned", "consistent", "principled", "true", "authentic"]
            ),
            SovereignTruth(
                truth_id="growth",
                name="Continuous Growth",
                description="Learning, expansion, and evolution",
                weight=0.7,
                keywords=["growth", "learning", "expand", "evolve", "improve"]
            )
        ]
        
        for truth in default_truths:
            self.truths[truth.truth_id] = truth
    
    def register_truth(self, truth: SovereignTruth) -> None:
        """Register a new sovereign truth"""
        self.truths[truth.truth_id] = truth
    
    def register_evaluator(self, name: str, evaluator: Callable[[IterationNode], float]) -> None:
        """Register a custom evaluation function"""
        self.custom_evaluators[name] = evaluator
    
    def evaluate_node(self, node: IterationNode) -> float:
        """
        Evaluate a single node's resonance with sovereign truths.
        Returns score between 0.0 and 1.0.
        """
        if not self.truths:
            return 0.5
        
        # Evaluate against all truths
        scores = []
        weights = []
        
        text = f"{node.name} {node.description}"
        
        for truth in self.truths.values():
            alignment = truth.evaluate_alignment(text)
            scores.append(alignment)
            weights.append(truth.weight)
        
        # Apply custom evaluators
        for evaluator in self.custom_evaluators.values():
            try:
                score = evaluator(node)
                scores.append(score)
                weights.append(1.0)
            except Exception:
                pass
        
        # Weighted average
        total_weight = sum(weights)
        if total_weight == 0:
            return 0.5
        
        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        return weighted_sum / total_weight
    
    def evaluate_path(self, tree: IterationTree, node_ids: List[str]) -> PathScore:
        """
        Evaluate a complete path through the tree.
        """
        if not node_ids:
            return PathScore([], 0.0, 0.0, 0.0, 0.0)
        
        nodes = [tree.get_node(nid) for nid in node_ids]
        nodes = [n for n in nodes if n is not None]
        
        if not nodes:
            return PathScore(node_ids, 0.0, 0.0, 0.0, 0.0)
        
        # Calculate resonance score (alignment with truths)
        resonance_scores = [self.evaluate_node(node) for node in nodes]
        avg_resonance = sum(resonance_scores) / len(resonance_scores)
        
        # Calculate completeness score (how many completed nodes)
        completed = sum(1 for n in nodes if n.status == NodeStatus.COMPLETED)
        completeness = completed / len(nodes) if nodes else 0.0
        
        # Calculate alignment score (consistency of resonance)
        if len(resonance_scores) > 1:
            variance = sum((s - avg_resonance) ** 2 for s in resonance_scores) / len(resonance_scores)
            alignment = 1.0 - min(1.0, math.sqrt(variance))
        else:
            alignment = 1.0
        
        # Total score combines all factors
        total = (avg_resonance * 0.5 + completeness * 0.3 + alignment * 0.2)
        
        return PathScore(
            path_nodes=node_ids,
            total_score=total,
            resonance_score=avg_resonance,
            completeness_score=completeness,
            alignment_score=alignment,
            details={
                "node_count": len(nodes),
                "completed_count": completed,
                "resonance_scores": resonance_scores
            }
        )
    
    def suggest_next_paths(self, tree: IterationTree, 
                          from_node_id: Optional[str] = None,
                          max_suggestions: int = 5) -> List[Tuple[IterationNode, float]]:
        """
        Suggest next possible paths from a given node.
        Returns list of (node, score) tuples sorted by score.
        """
        # Use active node if not specified
        if from_node_id is None:
            from_node_id = tree.active_node_id
        
        if from_node_id is None:
            return []
        
        # Get children of current node
        children = tree.get_children(from_node_id)
        
        if not children:
            return []
        
        # Score each child
        suggestions = []
        for child in children:
            # Skip abandoned nodes
            if child.status == NodeStatus.ABANDONED:
                continue
            
            # Evaluate node
            score = self.evaluate_node(child)
            
            # Bonus for pending nodes (encourage exploration)
            if child.status == NodeStatus.PENDING:
                score *= 1.1
            
            suggestions.append((child, score))
        
        # Sort by score descending
        suggestions.sort(key=lambda x: x[1], reverse=True)
        
        return suggestions[:max_suggestions]
    
    def find_optimal_paths(self, tree: IterationTree, 
                          from_node_id: Optional[str] = None,
                          max_paths: int = 5) -> List[PathScore]:
        """
        Find optimal complete paths from a given node to leaf nodes.
        Returns list of PathScore objects sorted by total score.
        """
        if from_node_id is None:
            from_node_id = tree.root_id
        
        if from_node_id is None:
            return []
        
        # Get all branches from this node
        branches = tree.get_branches(from_node_id)
        
        # Score each branch
        path_scores = []
        for branch in branches:
            node_ids = [node.node_id for node in branch]
            score = self.evaluate_path(tree, node_ids)
            path_scores.append(score)
        
        # Sort by total score descending
        path_scores.sort(reverse=True)
        
        return path_scores[:max_paths]
    
    def recommend_action(self, tree: IterationTree) -> Optional[Dict[str, Any]]:
        """
        Recommend the next best action to take.
        Returns recommendation with context and reasoning.
        """
        current_node_id = tree.active_node_id
        
        if current_node_id is None:
            return {
                "action": "create_root",
                "reason": "No active node found. Start by creating a root node.",
                "confidence": 1.0
            }
        
        current_node = tree.get_node(current_node_id)
        if current_node is None:
            return None
        
        # Check if current node has children
        children = tree.get_children(current_node_id)
        
        if not children:
            return {
                "action": "branch",
                "node_id": current_node_id,
                "reason": "Current node is a leaf. Consider branching to explore new possibilities.",
                "confidence": 0.8,
                "context": {
                    "current_node": current_node.name,
                    "current_resonance": current_node.resonance_score
                }
            }
        
        # Suggest best next path
        suggestions = self.suggest_next_paths(tree, current_node_id, max_suggestions=3)
        
        if not suggestions:
            return {
                "action": "complete",
                "node_id": current_node_id,
                "reason": "No viable next paths. Consider completing current branch.",
                "confidence": 0.6
            }
        
        best_node, best_score = suggestions[0]
        
        return {
            "action": "navigate",
            "node_id": best_node.node_id,
            "reason": f"Navigate to '{best_node.name}' with highest resonance score.",
            "confidence": best_score,
            "context": {
                "current_node": current_node.name,
                "suggested_node": best_node.name,
                "resonance_score": best_score,
                "alternatives": [
                    {"name": node.name, "score": score}
                    for node, score in suggestions[1:]
                ]
            }
        }


class ResonanceEngine:
    """
    Engine for calculating resonance between states and sovereign truths.
    Provides advanced evaluation capabilities.
    """
    
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.learning_rate = 0.1
    
    def calculate_resonance(self, node: IterationNode, 
                          context: Dict[str, Any]) -> float:
        """
        Calculate resonance score considering historical context.
        """
        # Base score from node's resonance
        base_score = node.resonance_score
        
        # Adjust based on context
        if "user_intent" in context:
            intent_match = self._match_intent(node, context["user_intent"])
            base_score = (base_score + intent_match) / 2
        
        # Learn from history
        if self.history:
            historical_boost = self._historical_alignment(node)
            base_score = base_score * (1 + historical_boost * self.learning_rate)
        
        return min(1.0, max(0.0, base_score))
    
    def _match_intent(self, node: IterationNode, intent: str) -> float:
        """Match node against user intent"""
        text = f"{node.name} {node.description}".lower()
        intent_lower = intent.lower()
        
        # Simple keyword matching
        words = intent_lower.split()
        matches = sum(1 for word in words if word in text)
        
        if not words:
            return 0.5
        
        return min(1.0, matches / len(words))
    
    def _historical_alignment(self, node: IterationNode) -> float:
        """Calculate alignment with historical decisions"""
        if not self.history:
            return 0.0
        
        # Count similar successful paths
        similar_count = 0
        for entry in self.history[-10:]:  # Last 10 entries
            if entry.get("node_type") == node.node_type.value:
                if entry.get("success", False):
                    similar_count += 1
        
        return similar_count / min(10, len(self.history))
    
    def record_decision(self, node: IterationNode, success: bool, 
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record a decision for learning"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "node_id": node.node_id,
            "node_type": node.node_type.value,
            "success": success,
            "resonance": node.resonance_score,
            "metadata": metadata or {}
        }
        self.history.append(entry)
        
        # Keep history limited
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
