"""
Sovereign Workflow Manager
Integrates the sovereign iteration framework with Apollo's workflow and task orchestration.
Records sovereign choices as part of Apollo's shared memory.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json

from core.sovereign_iteration_framework import (
    IterationTree, IterationNode, NodeType, NodeStatus,
    SovereignIterationManager
)
from core.sovereign_path_optimizer import PathOptimizer, SovereignTruth


@dataclass
class WorkflowTask:
    """
    Represents a task in Apollo's workflow.
    """
    task_id: str
    name: str
    description: str
    status: str = "pending"
    priority: int = 1
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SovereignChoice:
    """
    Represents a sovereign choice made by Apollo.
    Stored as part of Apollo's memory and evolution.
    """
    choice_id: str
    tree_id: str
    from_node_id: str
    to_node_id: str
    rationale: str
    resonance_score: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class SovereignWorkflowManager:
    """
    Manages integration of sovereign iteration framework with workflows.
    Orchestrates branching processes and records sovereign choices.
    """
    
    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or Path.home() / ".apollo_sovereign_workflows"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.iteration_manager = SovereignIterationManager(self.storage_dir / "iterations")
        self.path_optimizer = PathOptimizer()
        
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.tasks: Dict[str, WorkflowTask] = {}
        self.choices: List[SovereignChoice] = []
        
        self.task_handlers: Dict[str, Callable] = {}
        
        # Memory integration
        self.memory_file = self.storage_dir / "sovereign_memory.json"
        self.load_memory()
    
    def create_workflow(self, workflow_id: str, name: str, 
                       description: str) -> IterationTree:
        """
        Create a new workflow with associated iteration tree.
        """
        # Create iteration tree
        tree = self.iteration_manager.create_tree(
            tree_id=workflow_id,
            root_name=name,
            root_description=description
        )
        
        # Register workflow
        self.workflows[workflow_id] = {
            "workflow_id": workflow_id,
            "name": name,
            "description": description,
            "tree_id": workflow_id,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        return tree
    
    def add_workflow_step(self, workflow_id: str, parent_step_id: str,
                         step_id: str, name: str, description: str,
                         step_type: NodeType = NodeType.ACTION,
                         metadata: Optional[Dict[str, Any]] = None) -> IterationNode:
        """
        Add a step to a workflow.
        """
        tree = self.iteration_manager.get_tree(workflow_id)
        if tree is None:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Add node to tree
        node = tree.add_node(
            parent_id=parent_step_id,
            node_id=step_id,
            name=name,
            description=description,
            node_type=step_type,
            metadata=metadata
        )
        
        # Evaluate resonance
        resonance = self.path_optimizer.evaluate_node(node)
        node.set_resonance(resonance)
        
        return node
    
    def execute_step(self, workflow_id: str, step_id: str,
                    context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a workflow step.
        """
        tree = self.iteration_manager.get_tree(workflow_id)
        if tree is None:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        node = tree.get_node(step_id)
        if node is None:
            raise ValueError(f"Step {step_id} not found")
        
        # Set as active node
        tree.set_active_node(step_id)
        
        # Execute if handler registered
        result = {"status": "executed", "step_id": step_id}
        
        handler_key = f"{workflow_id}:{step_id}"
        if handler_key in self.task_handlers:
            try:
                handler_result = self.task_handlers[handler_key](node, context or {})
                result["handler_result"] = handler_result
            except Exception as e:
                result["error"] = str(e)
                node.update_status(NodeStatus.ABANDONED)
                return result
        
        # Mark as completed
        node.update_status(NodeStatus.COMPLETED)
        
        return result
    
    def branch_workflow(self, workflow_id: str, from_step_id: str,
                       branches: List[Dict[str, str]]) -> List[IterationNode]:
        """
        Create multiple branches from a step.
        
        Args:
            workflow_id: ID of the workflow
            from_step_id: ID of the step to branch from
            branches: List of dicts with 'step_id', 'name', 'description'
        
        Returns:
            List of created branch nodes
        """
        tree = self.iteration_manager.get_tree(workflow_id)
        if tree is None:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        created_nodes = []
        
        for branch_spec in branches:
            node = self.add_workflow_step(
                workflow_id=workflow_id,
                parent_step_id=from_step_id,
                step_id=branch_spec["step_id"],
                name=branch_spec["name"],
                description=branch_spec["description"],
                step_type=NodeType.DECISION,
                metadata=branch_spec.get("metadata", {})
            )
            created_nodes.append(node)
        
        return created_nodes
    
    def choose_path(self, workflow_id: str, from_step_id: str,
                   to_step_id: str, rationale: str) -> SovereignChoice:
        """
        Make a sovereign choice between branches.
        Records the choice in Apollo's memory.
        """
        tree = self.iteration_manager.get_tree(workflow_id)
        if tree is None:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        from_node = tree.get_node(from_step_id)
        to_node = tree.get_node(to_step_id)
        
        if from_node is None or to_node is None:
            raise ValueError("Invalid node IDs")
        
        # Create choice record
        choice = SovereignChoice(
            choice_id=f"{workflow_id}:{from_step_id}:{to_step_id}",
            tree_id=workflow_id,
            from_node_id=from_step_id,
            to_node_id=to_step_id,
            rationale=rationale,
            resonance_score=to_node.resonance_score
        )
        
        self.choices.append(choice)
        
        # Set as active path
        tree.set_active_node(to_step_id)
        
        # Save to memory
        self.save_memory()
        
        return choice
    
    def get_next_steps(self, workflow_id: str,
                      max_suggestions: int = 5) -> List[Dict[str, Any]]:
        """
        Get suggested next steps for a workflow.
        """
        tree = self.iteration_manager.get_tree(workflow_id)
        if tree is None:
            return []
        
        suggestions = self.path_optimizer.suggest_next_paths(
            tree, max_suggestions=max_suggestions
        )
        
        return [
            {
                "step_id": node.node_id,
                "name": node.name,
                "description": node.description,
                "resonance_score": score,
                "status": node.status.value
            }
            for node, score in suggestions
        ]
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get comprehensive status of a workflow.
        """
        tree = self.iteration_manager.get_tree(workflow_id)
        if tree is None:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows.get(workflow_id, {})
        stats = tree.get_statistics()
        active_path = tree.get_active_path()
        
        return {
            "workflow_id": workflow_id,
            "name": workflow.get("name", "Unknown"),
            "status": workflow.get("status", "unknown"),
            "statistics": stats,
            "active_path": [
                {"step_id": node.node_id, "name": node.name}
                for node in active_path
            ],
            "next_suggestions": self.get_next_steps(workflow_id, max_suggestions=3)
        }
    
    def register_task_handler(self, workflow_id: str, step_id: str,
                             handler: Callable) -> None:
        """
        Register a handler function for a specific workflow step.
        """
        key = f"{workflow_id}:{step_id}"
        self.task_handlers[key] = handler
    
    def integrate_with_task(self, task: WorkflowTask, workflow_id: str) -> IterationNode:
        """
        Integrate an existing task with a workflow.
        """
        tree = self.iteration_manager.get_tree(workflow_id)
        if tree is None:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Add task as node
        parent_id = tree.active_node_id or tree.root_id
        
        node = self.add_workflow_step(
            workflow_id=workflow_id,
            parent_step_id=parent_id,
            step_id=task.task_id,
            name=task.name,
            description=task.description,
            metadata={"priority": task.priority, "dependencies": task.dependencies}
        )
        
        self.tasks[task.task_id] = task
        
        return node
    
    def save_memory(self) -> None:
        """
        Save sovereign choices and workflow state to memory.
        """
        memory_data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "workflows": self.workflows,
            "choices": [
                {
                    "choice_id": choice.choice_id,
                    "tree_id": choice.tree_id,
                    "from_node_id": choice.from_node_id,
                    "to_node_id": choice.to_node_id,
                    "rationale": choice.rationale,
                    "resonance_score": choice.resonance_score,
                    "timestamp": choice.timestamp,
                    "metadata": choice.metadata
                }
                for choice in self.choices
            ],
            "statistics": {
                "total_workflows": len(self.workflows),
                "total_choices": len(self.choices),
                "active_workflows": sum(
                    1 for w in self.workflows.values()
                    if w.get("status") == "active"
                )
            }
        }
        
        with open(self.memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
        
        # Save all trees
        for tree_id in self.iteration_manager.list_trees():
            self.iteration_manager.save_tree(tree_id)
    
    def load_memory(self) -> None:
        """
        Load sovereign choices and workflow state from memory.
        """
        if not self.memory_file.exists():
            return
        
        try:
            with open(self.memory_file, 'r') as f:
                memory_data = json.load(f)
            
            self.workflows = memory_data.get("workflows", {})
            
            # Reconstruct choices
            self.choices = [
                SovereignChoice(
                    choice_id=c["choice_id"],
                    tree_id=c["tree_id"],
                    from_node_id=c["from_node_id"],
                    to_node_id=c["to_node_id"],
                    rationale=c["rationale"],
                    resonance_score=c["resonance_score"],
                    timestamp=c["timestamp"],
                    metadata=c.get("metadata", {})
                )
                for c in memory_data.get("choices", [])
            ]
            
            # Load trees
            for tree_id in self.iteration_manager.list_saved_trees():
                try:
                    self.iteration_manager.load_tree(tree_id)
                except Exception:
                    pass
                    
        except Exception:
            pass
    
    def export_workflow_history(self, workflow_id: str) -> Dict[str, Any]:
        """
        Export complete history of a workflow for analysis.
        """
        tree = self.iteration_manager.get_tree(workflow_id)
        if tree is None:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows.get(workflow_id, {})
        workflow_choices = [c for c in self.choices if c.tree_id == workflow_id]
        
        return {
            "workflow": workflow,
            "tree": tree.to_dict(),
            "choices": [
                {
                    "from": c.from_node_id,
                    "to": c.to_node_id,
                    "rationale": c.rationale,
                    "resonance": c.resonance_score,
                    "timestamp": c.timestamp
                }
                for c in workflow_choices
            ],
            "statistics": tree.get_statistics()
        }
