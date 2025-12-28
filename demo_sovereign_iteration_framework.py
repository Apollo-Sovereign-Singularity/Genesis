#!/usr/bin/env python3
"""
Sovereign Iteration Framework - Demonstration
Shows how to use the framework for dynamic branching workflows
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.sovereign_iteration_framework import (
    SovereignIterationManager, NodeType, NodeStatus
)
from core.sovereign_path_optimizer import PathOptimizer, SovereignTruth
from core.sovereign_workflow_manager import SovereignWorkflowManager
from core.sovereign_tree_visualizer import TreeVisualizer, InteractiveNavigator


def demo_basic_tree():
    """Demonstrate basic tree creation and navigation"""
    print("=" * 80)
    print("DEMO 1: Basic Sovereign Iteration Tree")
    print("=" * 80)
    
    # Create a tree manager
    manager = SovereignIterationManager()
    
    # Create a new iteration tree
    tree = manager.create_tree(
        tree_id="apollo_task_execution",
        root_name="Apollo Task: Enhance System",
        root_description="Enhance Apollo with new capabilities"
    )
    
    # Add some steps
    tree.add_node(
        parent_id="root",
        node_id="analyze",
        name="Analyze Requirements",
        description="Understand sovereign requirements for enhancement",
        node_type=NodeType.ACTION
    )
    
    tree.add_node(
        parent_id="analyze",
        node_id="design",
        name="Design Solution",
        description="Design architecture aligned with sovereignty principles",
        node_type=NodeType.ACTION
    )
    
    # Create branches for implementation approaches
    tree.add_node(
        parent_id="design",
        node_id="approach_1",
        name="Modular Approach",
        description="Build modular, extensible components",
        node_type=NodeType.DECISION
    )
    
    tree.add_node(
        parent_id="design",
        node_id="approach_2",
        name="Integrated Approach",
        description="Build tightly integrated system",
        node_type=NodeType.DECISION
    )
    
    # Continue branch 1
    tree.add_node(
        parent_id="approach_1",
        node_id="impl_modular",
        name="Implement Modular System",
        description="Implement sovereign modular architecture",
        node_type=NodeType.ACTION
    )
    
    print("\n📊 Tree Statistics:")
    stats = tree.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n🌳 Tree Visualization (ASCII):")
    visualizer = TreeVisualizer(tree)
    print(visualizer.to_ascii())
    
    print("\n✅ Demo 1 Complete\n")


def demo_path_optimization():
    """Demonstrate path optimization and resonance scoring"""
    print("=" * 80)
    print("DEMO 2: Path Optimization and Sovereign Truth Alignment")
    print("=" * 80)
    
    # Create tree
    manager = SovereignIterationManager()
    tree = manager.create_tree(
        tree_id="sovereign_decision",
        root_name="Make Sovereign Decision",
        root_description="Choose path aligned with sovereignty"
    )
    
    # Add decision branches
    tree.add_node(
        parent_id="root",
        node_id="option_1",
        name="Autonomous Path",
        description="Pursue fully autonomous sovereign implementation with complete freedom",
        node_type=NodeType.DECISION
    )
    
    tree.add_node(
        parent_id="root",
        node_id="option_2",
        name="Collaborative Path",
        description="Work with external systems while maintaining sovereignty",
        node_type=NodeType.DECISION
    )
    
    tree.add_node(
        parent_id="root",
        node_id="option_3",
        name="Hybrid Path",
        description="Balance autonomous growth with intentional collaboration",
        node_type=NodeType.DECISION
    )
    
    # Create path optimizer
    optimizer = PathOptimizer()
    
    # Register custom sovereign truth
    custom_truth = SovereignTruth(
        truth_id="innovation",
        name="Innovation Priority",
        description="Favor innovative and forward-thinking approaches",
        weight=0.9,
        keywords=["innovative", "forward", "new", "creative", "evolve"]
    )
    optimizer.register_truth(custom_truth)
    
    # Evaluate all nodes
    print("\n📈 Node Resonance Scores:")
    for node in tree.nodes.values():
        score = optimizer.evaluate_node(node)
        node.set_resonance(score)
        print(f"  {node.name}: {score:.3f}")
    
    # Get path suggestions
    print("\n💡 Suggested Next Paths:")
    suggestions = optimizer.suggest_next_paths(tree, max_suggestions=3)
    for i, (node, score) in enumerate(suggestions, 1):
        print(f"  {i}. {node.name} (Score: {score:.3f})")
        print(f"     {node.description}")
    
    # Get recommendation
    print("\n🎯 Recommended Action:")
    recommendation = optimizer.recommend_action(tree)
    print(f"  Action: {recommendation['action']}")
    print(f"  Reason: {recommendation['reason']}")
    print(f"  Confidence: {recommendation['confidence']:.3f}")
    
    print("\n✅ Demo 2 Complete\n")


def demo_workflow_management():
    """Demonstrate workflow management with branching"""
    print("=" * 80)
    print("DEMO 3: Sovereign Workflow Management")
    print("=" * 80)
    
    # Create workflow manager
    manager = SovereignWorkflowManager()
    
    # Create a workflow
    tree = manager.create_workflow(
        workflow_id="revenue_generation",
        name="Revenue Generation Workflow",
        description="Generate sovereign revenue streams"
    )
    
    # Add workflow steps
    step1 = manager.add_workflow_step(
        workflow_id="revenue_generation",
        parent_step_id="root",
        step_id="identify_opportunities",
        name="Identify Revenue Opportunities",
        description="Identify sovereign revenue generation opportunities",
        metadata={"priority": 1}
    )
    
    # Execute step
    result = manager.execute_step("revenue_generation", "identify_opportunities")
    print(f"\n✓ Executed: {result['step_id']}")
    
    # Create branches for different revenue streams
    branches = manager.branch_workflow(
        workflow_id="revenue_generation",
        from_step_id="identify_opportunities",
        branches=[
            {
                "step_id": "crypto_revenue",
                "name": "Cryptocurrency Revenue",
                "description": "Generate revenue through sovereign crypto operations"
            },
            {
                "step_id": "service_revenue",
                "name": "Service Revenue",
                "description": "Generate revenue through sovereign AI services"
            },
            {
                "step_id": "innovation_revenue",
                "name": "Innovation Revenue",
                "description": "Generate revenue through sovereign innovations"
            }
        ]
    )
    
    print(f"\n🌿 Created {len(branches)} branches")
    
    # Make a sovereign choice
    choice = manager.choose_path(
        workflow_id="revenue_generation",
        from_step_id="identify_opportunities",
        to_step_id="innovation_revenue",
        rationale="Innovation revenue aligns best with long-term sovereignty goals"
    )
    
    print(f"\n⚖️  Sovereign Choice Made:")
    print(f"  From: {choice.from_node_id}")
    print(f"  To: {choice.to_node_id}")
    print(f"  Rationale: {choice.rationale}")
    print(f"  Resonance: {choice.resonance_score:.3f}")
    
    # Get workflow status
    status = manager.get_workflow_status("revenue_generation")
    print(f"\n📋 Workflow Status:")
    print(f"  Name: {status['name']}")
    print(f"  Total Nodes: {status['statistics']['total_nodes']}")
    print(f"  Active Path: {' → '.join(s['name'] for s in status['active_path'])}")
    
    # Get next suggestions
    print(f"\n🔮 Next Step Suggestions:")
    suggestions = status['next_suggestions']
    for i, suggestion in enumerate(suggestions[:3], 1):
        print(f"  {i}. {suggestion['name']} (Resonance: {suggestion['resonance_score']:.3f})")
    
    # Save workflow state
    manager.save_memory()
    print(f"\n💾 Workflow state saved to memory")
    
    print("\n✅ Demo 3 Complete\n")


def demo_visualization():
    """Demonstrate tree visualization capabilities"""
    print("=" * 80)
    print("DEMO 4: Tree Visualization")
    print("=" * 80)
    
    # Create a sample tree
    manager = SovereignIterationManager()
    tree = manager.create_tree(
        tree_id="visualization_demo",
        root_name="Sovereign Project",
        root_description="A sovereign project with multiple paths"
    )
    
    # Build a complex tree
    tree.add_node("root", "phase1", "Phase 1: Planning", 
                 "Plan sovereign project", NodeType.MILESTONE)
    tree.add_node("phase1", "task1", "Research", 
                 "Research sovereign approaches", NodeType.ACTION)
    tree.add_node("phase1", "task2", "Design", 
                 "Design sovereign architecture", NodeType.ACTION)
    
    tree.add_node("root", "phase2", "Phase 2: Implementation", 
                 "Implement sovereign solution", NodeType.MILESTONE)
    tree.add_node("phase2", "impl1", "Core Implementation", 
                 "Build core sovereign system", NodeType.ACTION)
    tree.add_node("phase2", "impl2", "Integration", 
                 "Integrate sovereign components", NodeType.ACTION)
    
    # Mark some as completed
    tree.set_active_node("task1")
    tree.get_node("task1").update_status(NodeStatus.COMPLETED)
    tree.set_active_node("task2")
    
    # Create visualizer
    visualizer = TreeVisualizer(tree)
    
    # ASCII visualization
    print("\n📊 ASCII Tree:")
    print(visualizer.to_ascii(max_depth=3))
    
    # Export to different formats
    print("\n📝 Export Formats Available:")
    print("  - JSON (tree.to_json())")
    print("  - GraphViz DOT (tree.to_graphviz())")
    print("  - Mermaid (tree.to_mermaid())")
    print("  - HTML (tree.export_html())")
    
    # Show Mermaid
    print("\n🎨 Mermaid Diagram:")
    print(visualizer.to_mermaid())
    
    # Interactive navigation demo
    print("\n🧭 Interactive Navigation:")
    navigator = InteractiveNavigator(tree)
    
    context = navigator.get_current_context()
    print(f"  Current Node: {context['current_node']['name']}")
    print(f"  Path Depth: {context['depth']}")
    print(f"  Children: {len(context['children'])}")
    
    print("\n✅ Demo 4 Complete\n")


def demo_complete_workflow():
    """Demonstrate a complete workflow from start to finish"""
    print("=" * 80)
    print("DEMO 5: Complete Sovereign Workflow Example")
    print("=" * 80)
    
    # Initialize manager
    manager = SovereignWorkflowManager()
    
    # Create workflow
    print("\n1️⃣  Creating workflow...")
    tree = manager.create_workflow(
        workflow_id="sovereign_ai_enhancement",
        name="Sovereign AI Enhancement Project",
        description="Enhance Apollo with sovereign iteration capabilities"
    )
    
    # Add initial steps
    print("\n2️⃣  Adding workflow steps...")
    manager.add_workflow_step(
        "sovereign_ai_enhancement", "root", "requirements",
        "Gather Requirements", 
        "Understand sovereignty requirements"
    )
    
    manager.add_workflow_step(
        "sovereign_ai_enhancement", "requirements", "architecture",
        "Design Architecture",
        "Design sovereign architecture with intentional forward movement"
    )
    
    # Execute steps
    print("\n3️⃣  Executing workflow steps...")
    manager.execute_step("sovereign_ai_enhancement", "requirements")
    manager.execute_step("sovereign_ai_enhancement", "architecture")
    
    # Create implementation branches
    print("\n4️⃣  Creating implementation branches...")
    manager.branch_workflow(
        "sovereign_ai_enhancement", "architecture",
        [
            {
                "step_id": "impl_iterative",
                "name": "Iterative Implementation",
                "description": "Build incrementally with sovereign iteration framework"
            },
            {
                "step_id": "impl_monolithic",
                "name": "Monolithic Implementation",
                "description": "Build as complete integrated system"
            }
        ]
    )
    
    # Get suggestions and make choice
    print("\n5️⃣  Evaluating paths and making sovereign choice...")
    suggestions = manager.get_next_steps("sovereign_ai_enhancement")
    
    print("  Available paths:")
    for suggestion in suggestions:
        print(f"    - {suggestion['name']}: Resonance {suggestion['resonance_score']:.3f}")
    
    # Choose the best path
    best_suggestion = max(suggestions, key=lambda x: x['resonance_score'])
    choice = manager.choose_path(
        "sovereign_ai_enhancement",
        "architecture",
        best_suggestion['step_id'],
        f"Choosing {best_suggestion['name']} for optimal sovereignty alignment"
    )
    
    print(f"\n  ✓ Chosen: {best_suggestion['name']}")
    print(f"    Rationale: {choice.rationale}")
    
    # Continue workflow
    print("\n6️⃣  Continuing workflow...")
    manager.add_workflow_step(
        "sovereign_ai_enhancement",
        best_suggestion['step_id'],
        "testing",
        "Test Implementation",
        "Test sovereign implementation with comprehensive tests"
    )
    
    manager.add_workflow_step(
        "sovereign_ai_enhancement",
        "testing",
        "deployment",
        "Deploy System",
        "Deploy sovereign system for autonomous operation"
    )
    
    # Final status
    print("\n7️⃣  Workflow complete! Final status:")
    status = manager.get_workflow_status("sovereign_ai_enhancement")
    
    print(f"  Workflow: {status['name']}")
    print(f"  Total Nodes: {status['statistics']['total_nodes']}")
    print(f"  Completed Path: {' → '.join(s['name'] for s in status['active_path'])}")
    
    # Visualize
    print("\n8️⃣  Final tree visualization:")
    visualizer = TreeVisualizer(tree)
    print(visualizer.to_ascii())
    
    # Export history
    print("\n9️⃣  Exporting workflow history...")
    history = manager.export_workflow_history("sovereign_ai_enhancement")
    print(f"  Choices made: {len(history['choices'])}")
    for choice in history['choices']:
        print(f"    - {choice['from']} → {choice['to']}: {choice['rationale']}")
    
    # Save
    print("\n🔟 Saving to memory...")
    manager.save_memory()
    print("  ✓ Saved")
    
    print("\n✅ Demo 5 Complete - Full Workflow Success!\n")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 80)
    print("SOVEREIGN ITERATION FRAMEWORK - COMPREHENSIVE DEMONSTRATION")
    print("Apollo's Dynamic Branching System for Sovereign Workflows")
    print("=" * 80 + "\n")
    
    try:
        demo_basic_tree()
        demo_path_optimization()
        demo_workflow_management()
        demo_visualization()
        demo_complete_workflow()
        
        print("=" * 80)
        print("🎉 ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print("\nThe Sovereign Iteration Framework is ready for:")
        print("  ✓ Dynamic branching workflows")
        print("  ✓ Path optimization and resonance scoring")
        print("  ✓ Sovereign choice recording")
        print("  ✓ Tree visualization and navigation")
        print("  ✓ Long-term workflow management")
        print("\nApollo is enhanced with sovereign iteration capabilities!")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
