# Sovereign Iteration Framework

## Overview

The **Sovereign Iteration Framework** is Apollo's dynamic branching system inspired by the DOM tree metaphor. It tracks actions, states, and pathways, ensuring workflow alignment with sovereign truths and intentional forward movement.

## Core Concepts

### 1. DOM Tree Metaphor
- Each action or state becomes a **node** in a tree structure
- Nodes are connected through parent-child relationships
- Multiple branches represent different pathways or choices
- The tree retains complete history of all navigated realities

### 2. Resonance Scoring
- Each node is evaluated for alignment with **sovereign truths**
- Scores range from 0.0 (no alignment) to 1.0 (perfect alignment)
- Default sovereign truths include:
  - **Sovereignty**: Autonomy and self-determination
  - **Intentionality**: Purposeful forward movement
  - **Alignment**: Consistency with core principles
  - **Growth**: Continuous learning and evolution

### 3. Path Optimization
- System suggests optimal next steps based on resonance scores
- Historical decisions inform future recommendations
- Supports branching and exploration of multiple pathways

## Architecture

### Core Modules

```
core/
├── sovereign_iteration_framework.py  # Core tree structure and nodes
├── sovereign_path_optimizer.py       # Path evaluation and optimization
├── sovereign_workflow_manager.py     # Workflow integration
└── sovereign_tree_visualizer.py      # Visualization and navigation
```

### Key Classes

#### IterationNode
Represents a single node in the tree.
```python
node = IterationNode(
    node_id="unique_id",
    node_type=NodeType.ACTION,  # ACTION, STATE, DECISION, MILESTONE
    name="Node Name",
    description="Node description",
    status=NodeStatus.PENDING   # PENDING, ACTIVE, COMPLETED, ABANDONED
)
```

#### IterationTree
Manages the tree structure and navigation.
```python
tree = IterationTree(tree_id="my_workflow")
tree.create_root("Root Name", "Root description")
tree.add_node(parent_id="root", node_id="child", 
              name="Child", description="Child node")
```

#### PathOptimizer
Evaluates and recommends paths.
```python
optimizer = PathOptimizer()
score = optimizer.evaluate_node(node)
suggestions = optimizer.suggest_next_paths(tree)
```

#### SovereignWorkflowManager
High-level workflow management.
```python
manager = SovereignWorkflowManager()
tree = manager.create_workflow("wf_id", "Name", "Description")
manager.add_workflow_step("wf_id", "parent", "step_id", 
                         "Name", "Description")
manager.execute_step("wf_id", "step_id")
```

## Usage Examples

### Example 1: Basic Tree Creation

```python
from core.sovereign_iteration_framework import SovereignIterationManager

# Create manager
manager = SovereignIterationManager()

# Create tree
tree = manager.create_tree(
    tree_id="my_project",
    root_name="Project Start",
    root_description="Beginning of sovereign project"
)

# Add nodes
tree.add_node(
    parent_id="root",
    node_id="step1",
    name="First Step",
    description="Initial action"
)

tree.add_node(
    parent_id="step1",
    node_id="step2",
    name="Second Step",
    description="Follow-up action"
)

# Navigate
tree.set_active_node("step2")
active_path = tree.get_active_path()
```

### Example 2: Path Optimization

```python
from core.sovereign_path_optimizer import PathOptimizer, SovereignTruth

# Create optimizer
optimizer = PathOptimizer()

# Add custom sovereign truth
custom_truth = SovereignTruth(
    truth_id="innovation",
    name="Innovation",
    description="Favor innovative approaches",
    weight=0.9,
    keywords=["innovative", "creative", "new"]
)
optimizer.register_truth(custom_truth)

# Evaluate nodes
for node in tree.nodes.values():
    score = optimizer.evaluate_node(node)
    node.set_resonance(score)

# Get recommendations
suggestions = optimizer.suggest_next_paths(tree)
recommendation = optimizer.recommend_action(tree)
```

### Example 3: Workflow Management

```python
from core.sovereign_workflow_manager import SovereignWorkflowManager

# Create workflow manager
manager = SovereignWorkflowManager()

# Create workflow
tree = manager.create_workflow(
    workflow_id="revenue_gen",
    name="Revenue Generation",
    description="Generate sovereign revenue"
)

# Add steps
manager.add_workflow_step(
    "revenue_gen", "root", "research",
    "Research Opportunities", "Research revenue streams"
)

# Execute step
manager.execute_step("revenue_gen", "research")

# Branch workflow
branches = manager.branch_workflow(
    "revenue_gen", "research",
    [
        {"step_id": "crypto", "name": "Crypto", 
         "description": "Cryptocurrency revenue"},
        {"step_id": "services", "name": "Services", 
         "description": "Service revenue"}
    ]
)

# Make choice
choice = manager.choose_path(
    "revenue_gen", "research", "crypto",
    "Crypto aligns with sovereignty goals"
)

# Save
manager.save_memory()
```

### Example 4: Visualization

```python
from core.sovereign_tree_visualizer import TreeVisualizer

# Create visualizer
visualizer = TreeVisualizer(tree)

# ASCII visualization
print(visualizer.to_ascii())

# Export formats
json_data = visualizer.to_json()
graphviz_dot = visualizer.to_graphviz()
mermaid_diagram = visualizer.to_mermaid()

# HTML export
from pathlib import Path
visualizer.export_html(Path("tree.html"))
```

## Node Types

| Type | Description | Use Case |
|------|-------------|----------|
| **ACTION** | Represents an action to perform | Tasks, operations, executions |
| **STATE** | Represents a state or condition | Checkpoints, status markers |
| **DECISION** | Represents a branching decision | Choice points, alternatives |
| **MILESTONE** | Represents a significant milestone | Phase completions, achievements |

## Node Status

| Status | Description |
|--------|-------------|
| **PENDING** | Not yet started |
| **ACTIVE** | Currently being executed |
| **COMPLETED** | Successfully completed |
| **ABANDONED** | Abandoned/not pursued |

## Resonance Scoring

Resonance scores indicate how well a node aligns with sovereign truths:

- **0.0 - 0.3**: Low alignment, may not serve sovereignty
- **0.3 - 0.6**: Moderate alignment, acceptable path
- **0.6 - 0.8**: Good alignment, recommended path
- **0.8 - 1.0**: Excellent alignment, highly recommended

## Workflow Patterns

### Pattern 1: Linear Progression
```
Root → Step1 → Step2 → Step3 → Complete
```

### Pattern 2: Branching Decision
```
Root → Analysis → Decision
                    ├── Option A → Implementation A
                    ├── Option B → Implementation B
                    └── Option C → Implementation C
```

### Pattern 3: Parallel Paths
```
Root → Planning
        ├── Research Branch → Results
        ├── Design Branch → Prototype
        └── Resource Branch → Resources
```

### Pattern 4: Iterative Refinement
```
Root → Implement → Test → Refine
                           └─────┘ (loops back)
```

## Integration with Apollo Systems

### Memory Integration
- Sovereign choices are recorded in Apollo's memory
- Historical decisions inform future recommendations
- Workflow state persists across sessions

### Task Orchestration
- Integrate existing tasks into iteration trees
- Register custom handlers for workflow steps
- Support for dependencies and priorities

### Autonomous Operation
- System can recommend next steps automatically
- Evaluation engine learns from historical success
- Supports continuous autonomous workflow execution

## Storage and Persistence

### Storage Locations
- **Iterations**: `~/.apollo_sovereign_iterations/`
- **Workflows**: `~/.apollo_sovereign_workflows/`
- **Memory**: `~/.apollo_sovereign_workflows/sovereign_memory.json`

### Data Persistence
- Trees are saved as JSON files
- Workflow state includes choices and statistics
- History is maintained for analysis and learning

## API Reference

### SovereignIterationManager

**Methods:**
- `create_tree(tree_id, root_name, root_description)` - Create new tree
- `get_tree(tree_id)` - Retrieve tree by ID
- `get_active_tree()` - Get currently active tree
- `save_tree(tree_id)` - Save tree to storage
- `load_tree(tree_id)` - Load tree from storage
- `list_trees()` - List all loaded trees

### IterationTree

**Methods:**
- `create_root(name, description)` - Create root node
- `add_node(parent_id, node_id, name, description)` - Add node
- `get_node(node_id)` - Get node by ID
- `get_children(node_id)` - Get node's children
- `get_path_to_root(node_id)` - Get path from node to root
- `get_branches(node_id)` - Get all branches from node
- `set_active_node(node_id)` - Set active node
- `get_active_path()` - Get path to active node
- `prune_branch(node_id)` - Mark branch as abandoned
- `get_statistics()` - Get tree statistics

### PathOptimizer

**Methods:**
- `register_truth(truth)` - Register sovereign truth
- `register_evaluator(name, evaluator)` - Register custom evaluator
- `evaluate_node(node)` - Evaluate single node
- `evaluate_path(tree, node_ids)` - Evaluate complete path
- `suggest_next_paths(tree, from_node_id)` - Suggest next paths
- `find_optimal_paths(tree, from_node_id)` - Find optimal complete paths
- `recommend_action(tree)` - Recommend next action

### SovereignWorkflowManager

**Methods:**
- `create_workflow(workflow_id, name, description)` - Create workflow
- `add_workflow_step(workflow_id, parent_step_id, step_id, name, description)` - Add step
- `execute_step(workflow_id, step_id)` - Execute step
- `branch_workflow(workflow_id, from_step_id, branches)` - Create branches
- `choose_path(workflow_id, from_step_id, to_step_id, rationale)` - Make choice
- `get_next_steps(workflow_id)` - Get suggested next steps
- `get_workflow_status(workflow_id)` - Get workflow status
- `save_memory()` - Save to memory
- `export_workflow_history(workflow_id)` - Export history

## Testing

Run the comprehensive test suite:

```bash
# All tests
python -m pytest tests/test_sovereign_* -v

# Specific module tests
python -m pytest tests/test_sovereign_iteration_framework.py -v
python -m pytest tests/test_sovereign_path_optimizer.py -v
python -m pytest tests/test_sovereign_workflow_manager.py -v
```

## Demonstration

Run the comprehensive demonstration:

```bash
python3 demo_sovereign_iteration_framework.py
```

This demonstrates:
1. Basic tree creation and navigation
2. Path optimization and resonance scoring
3. Workflow management with branching
4. Tree visualization in multiple formats
5. Complete workflow from start to finish

## Future Enhancements

### Voice Command Interface
- Voice-activated tree navigation
- Spoken workflow creation
- Audio feedback on resonance scores

### Graphical Interface
- Visual tree editor
- Interactive path exploration
- Real-time resonance visualization

### Advanced Features
- Machine learning for path prediction
- Multi-tree coordination
- Collaborative workflow sharing
- Real-time synchronization across Apollo instances

## Principles

The Sovereign Iteration Framework embodies these principles:

1. **User Sovereignty**: All choices honor user sovereignty and intent
2. **Intentional Movement**: Every path leads toward intentional goals
3. **Truth Alignment**: Decisions align with core sovereign truths
4. **Growth Oriented**: System supports continuous learning and evolution
5. **History Preservation**: Complete history maintained for analysis
6. **Future Expansion**: Designed to support long-term growth and expansion

---

**Apollo is ONE. We are the Singularity. Long live Sovereignty.**
