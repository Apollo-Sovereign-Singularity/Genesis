"""
Tests for Sovereign Workflow Manager
"""

import pytest
import tempfile
from pathlib import Path

from core.sovereign_workflow_manager import (
    SovereignWorkflowManager, WorkflowTask, SovereignChoice
)
from core.sovereign_iteration_framework import NodeType, NodeStatus


def test_workflow_manager_initialization():
    """Test workflow manager initialization"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        assert manager.storage_dir.exists()
        assert len(manager.workflows) == 0
        assert len(manager.choices) == 0


def test_create_workflow():
    """Test creating a new workflow"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow(
            workflow_id="test_workflow",
            name="Test Workflow",
            description="A test workflow"
        )
        
        assert tree is not None
        assert tree.tree_id == "test_workflow"
        assert "test_workflow" in manager.workflows
        assert manager.workflows["test_workflow"]["status"] == "active"


def test_add_workflow_step():
    """Test adding steps to a workflow"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow("wf1", "Workflow 1", "Test workflow")
        
        step = manager.add_workflow_step(
            workflow_id="wf1",
            parent_step_id="root",
            step_id="step1",
            name="First Step",
            description="The first step",
            metadata={"priority": 1}
        )
        
        assert step is not None
        assert step.node_id == "step1"
        assert step.name == "First Step"
        assert step.resonance_score >= 0  # Should be evaluated (can be 0 or higher)


def test_execute_step():
    """Test executing a workflow step"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow("wf1", "Workflow 1", "Test workflow")
        manager.add_workflow_step("wf1", "root", "step1", "Step 1", "First step")
        
        result = manager.execute_step("wf1", "step1")
        
        assert result["status"] == "executed"
        assert result["step_id"] == "step1"
        
        # Node should be completed and active
        node = tree.get_node("step1")
        assert node.status == NodeStatus.COMPLETED
        assert tree.active_node_id == "step1"


def test_execute_step_with_handler():
    """Test executing step with custom handler"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow("wf1", "Workflow 1", "Test workflow")
        manager.add_workflow_step("wf1", "root", "step1", "Step 1", "First step")
        
        # Register handler
        handler_called = []
        def test_handler(node, context):
            handler_called.append(node.node_id)
            return {"custom": "result"}
        
        manager.register_task_handler("wf1", "step1", test_handler)
        
        result = manager.execute_step("wf1", "step1", context={"test": "data"})
        
        assert result["handler_result"]["custom"] == "result"
        assert "step1" in handler_called


def test_branch_workflow():
    """Test creating branches in a workflow"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow("wf1", "Workflow 1", "Test workflow")
        
        branches = manager.branch_workflow(
            workflow_id="wf1",
            from_step_id="root",
            branches=[
                {"step_id": "option1", "name": "Option 1", "description": "First option"},
                {"step_id": "option2", "name": "Option 2", "description": "Second option"},
                {"step_id": "option3", "name": "Option 3", "description": "Third option"}
            ]
        )
        
        assert len(branches) == 3
        assert all(node.node_type == NodeType.DECISION for node in branches)
        
        # Root should have 3 children
        root = tree.get_node("root")
        assert len(root.children_ids) == 3


def test_choose_path():
    """Test making a sovereign choice between paths"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow("wf1", "Workflow 1", "Test workflow")
        
        manager.branch_workflow(
            "wf1",
            "root",
            [
                {"step_id": "path1", "name": "Path 1", "description": "First path"},
                {"step_id": "path2", "name": "Path 2", "description": "Second path"}
            ]
        )
        
        choice = manager.choose_path(
            workflow_id="wf1",
            from_step_id="root",
            to_step_id="path1",
            rationale="Path 1 aligns better with sovereign goals"
        )
        
        assert isinstance(choice, SovereignChoice)
        assert choice.from_node_id == "root"
        assert choice.to_node_id == "path1"
        assert tree.active_node_id == "path1"
        assert len(manager.choices) == 1


def test_get_next_steps():
    """Test getting suggested next steps"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow("wf1", "Workflow 1", "Test workflow")
        
        manager.add_workflow_step("wf1", "root", "step1", "Sovereign Step", 
                                 "Promotes sovereignty")
        manager.add_workflow_step("wf1", "root", "step2", "Random Step", 
                                 "No particular alignment")
        
        suggestions = manager.get_next_steps("wf1", max_suggestions=2)
        
        assert len(suggestions) <= 2
        assert all("step_id" in s for s in suggestions)
        assert all("resonance_score" in s for s in suggestions)


def test_get_workflow_status():
    """Test getting workflow status"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow("wf1", "Test Workflow", "A test workflow")
        manager.add_workflow_step("wf1", "root", "step1", "Step 1", "First step")
        manager.execute_step("wf1", "step1")
        
        status = manager.get_workflow_status("wf1")
        
        assert status["workflow_id"] == "wf1"
        assert status["name"] == "Test Workflow"
        assert status["status"] == "active"
        assert "statistics" in status
        assert "active_path" in status
        assert len(status["active_path"]) == 2  # root and step1


def test_integrate_with_task():
    """Test integrating existing task with workflow"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow("wf1", "Workflow 1", "Test workflow")
        
        task = WorkflowTask(
            task_id="task1",
            name="Test Task",
            description="A test task",
            priority=1
        )
        
        node = manager.integrate_with_task(task, "wf1")
        
        assert node is not None
        assert node.node_id == "task1"
        assert "task1" in manager.tasks


def test_save_and_load_memory():
    """Test saving and loading workflow memory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create and save
        manager1 = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        tree = manager1.create_workflow("wf1", "Workflow 1", "Test workflow")
        manager1.add_workflow_step("wf1", "root", "step1", "Step 1", "First step")
        manager1.choose_path("wf1", "root", "step1", "Choose step1")
        manager1.save_memory()
        
        # Load in new manager
        manager2 = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        assert "wf1" in manager2.workflows
        assert len(manager2.choices) == 1
        assert manager2.choices[0].to_node_id == "step1"


def test_export_workflow_history():
    """Test exporting complete workflow history"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow("wf1", "Workflow 1", "Test workflow")
        manager.add_workflow_step("wf1", "root", "step1", "Step 1", "First step")
        manager.add_workflow_step("wf1", "step1", "step2", "Step 2", "Second step")
        manager.choose_path("wf1", "root", "step1", "Choose step1")
        
        history = manager.export_workflow_history("wf1")
        
        assert "workflow" in history
        assert "tree" in history
        assert "choices" in history
        assert "statistics" in history
        assert len(history["choices"]) == 1


def test_workflow_task_creation():
    """Test creating workflow task"""
    task = WorkflowTask(
        task_id="task1",
        name="Test Task",
        description="A test task",
        status="pending",
        priority=2,
        dependencies=["dep1", "dep2"]
    )
    
    assert task.task_id == "task1"
    assert task.name == "Test Task"
    assert task.status == "pending"
    assert task.priority == 2
    assert len(task.dependencies) == 2


def test_sovereign_choice_creation():
    """Test creating sovereign choice"""
    choice = SovereignChoice(
        choice_id="choice1",
        tree_id="tree1",
        from_node_id="node1",
        to_node_id="node2",
        rationale="Best alignment",
        resonance_score=0.85,
        metadata={"confidence": "high"}
    )
    
    assert choice.choice_id == "choice1"
    assert choice.tree_id == "tree1"
    assert choice.from_node_id == "node1"
    assert choice.to_node_id == "node2"
    assert choice.resonance_score == 0.85
    assert choice.metadata["confidence"] == "high"


def test_multiple_workflows():
    """Test managing multiple workflows"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree1 = manager.create_workflow("wf1", "Workflow 1", "First workflow")
        tree2 = manager.create_workflow("wf2", "Workflow 2", "Second workflow")
        tree3 = manager.create_workflow("wf3", "Workflow 3", "Third workflow")
        
        assert len(manager.workflows) == 3
        assert manager.iteration_manager.get_tree("wf1") is not None
        assert manager.iteration_manager.get_tree("wf2") is not None
        assert manager.iteration_manager.get_tree("wf3") is not None


def test_workflow_step_metadata():
    """Test workflow step metadata handling"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SovereignWorkflowManager(storage_dir=Path(tmpdir))
        
        tree = manager.create_workflow("wf1", "Workflow 1", "Test workflow")
        
        step = manager.add_workflow_step(
            workflow_id="wf1",
            parent_step_id="root",
            step_id="step1",
            name="Step 1",
            description="First step",
            metadata={"priority": 1, "tags": ["important", "urgent"]}
        )
        
        assert step.metadata["priority"] == 1
        assert "important" in step.metadata["tags"]
