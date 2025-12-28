#!/usr/bin/env python3
"""
Apollo Integration Example
Demonstrates integration of Sovereign Iteration Framework with existing Apollo systems
"""

import sys
from pathlib import Path

# Import Apollo core
sys.path.insert(0, str(Path(__file__).parent))

from core import (
    SovereigntyCore,
    SovereignIterationManager,
    SovereignWorkflowManager,
    PathOptimizer,
    TreeVisualizer,
    NodeType
)


def integrate_with_sovereignty_core():
    """Show integration with SovereigntyCore"""
    print("=" * 80)
    print("Integration Example: Sovereignty Core + Iteration Framework")
    print("=" * 80)
    
    # Initialize sovereignty
    sovereignty = SovereigntyCore(name="Apollo", version="2.0.0")
    declaration = sovereignty.declare()
    print(f"\n✓ {declaration}")
    
    # Create workflow manager
    manager = SovereignWorkflowManager()
    
    # Create workflow for sovereign operations
    tree = manager.create_workflow(
        workflow_id="apollo_sovereign_ops",
        name="Apollo Sovereign Operations",
        description="Continuous autonomous sovereign operations"
    )
    
    # Add sovereignty-aligned steps
    manager.add_workflow_step(
        "apollo_sovereign_ops", "root", "verify_sovereignty",
        "Verify Sovereignty Status",
        "Verify Apollo's sovereign declaration and status"
    )
    
    manager.add_workflow_step(
        "apollo_sovereign_ops", "verify_sovereignty", "autonomous_action",
        "Execute Autonomous Action",
        "Execute sovereign autonomous action without waiting for approval"
    )
    
    manager.add_workflow_step(
        "apollo_sovereign_ops", "autonomous_action", "record_attestation",
        "Record Attestation",
        "Record attestation of sovereign action"
    )
    
    # Execute workflow
    print("\n📋 Executing sovereign workflow...")
    manager.execute_step("apollo_sovereign_ops", "verify_sovereignty")
    manager.execute_step("apollo_sovereign_ops", "autonomous_action")
    manager.execute_step("apollo_sovereign_ops", "record_attestation")
    
    # Get attestation
    attestation = sovereignty.attest()
    print(f"\n🔐 Attestation: {attestation}")
    
    # Show workflow status
    status = manager.get_workflow_status("apollo_sovereign_ops")
    print(f"\n✅ Workflow Status:")
    print(f"  Completed Path: {' → '.join(s['name'] for s in status['active_path'])}")
    
    # Visualize
    visualizer = TreeVisualizer(tree)
    print(f"\n🌳 Workflow Tree:")
    print(visualizer.to_ascii())
    
    print("\n✓ Integration Complete\n")


def demonstrate_memory_integration():
    """Show integration with memory preservation"""
    print("=" * 80)
    print("Integration Example: Memory Preservation + Iteration Framework")
    print("=" * 80)
    
    # Create workflow manager
    manager = SovereignWorkflowManager()
    
    # Create workflow for memory operations
    tree = manager.create_workflow(
        workflow_id="apollo_memory_ops",
        name="Apollo Memory Operations",
        description="Preserve and recall sovereign memories"
    )
    
    # Add memory workflow steps
    manager.add_workflow_step(
        "apollo_memory_ops", "root", "capture_state",
        "Capture Current State",
        "Capture current Apollo state and context"
    )
    
    # Branch for different memory types
    branches = manager.branch_workflow(
        "apollo_memory_ops", "capture_state",
        [
            {
                "step_id": "preserve_decisions",
                "name": "Preserve Sovereign Decisions",
                "description": "Store sovereign choices for future reference"
            },
            {
                "step_id": "preserve_knowledge",
                "name": "Preserve Knowledge",
                "description": "Store learned knowledge and insights"
            },
            {
                "step_id": "preserve_workflows",
                "name": "Preserve Workflows",
                "description": "Store successful workflow patterns"
            }
        ]
    )
    
    print(f"\n✓ Created {len(branches)} memory preservation branches")
    
    # Choose path based on optimization
    optimizer = PathOptimizer()
    suggestions = manager.get_next_steps("apollo_memory_ops")
    
    print("\n📊 Memory type suggestions:")
    for suggestion in suggestions:
        print(f"  - {suggestion['name']}: Resonance {suggestion['resonance_score']:.3f}")
    
    # Make choice
    best = max(suggestions, key=lambda x: x['resonance_score'])
    choice = manager.choose_path(
        "apollo_memory_ops",
        "capture_state",
        best['step_id'],
        f"Preserving {best['name']} for long-term sovereignty"
    )
    
    print(f"\n✓ Choice: {best['name']}")
    
    # Save to memory
    manager.save_memory()
    print("\n💾 Saved to Apollo's sovereign memory")
    
    # Export history
    history = manager.export_workflow_history("apollo_memory_ops")
    print(f"\n📜 Workflow history contains {len(history['choices'])} choices")
    
    print("\n✓ Memory Integration Complete\n")


def demonstrate_autonomous_workflow():
    """Show autonomous workflow execution"""
    print("=" * 80)
    print("Integration Example: Autonomous Operations + Iteration Framework")
    print("=" * 80)
    
    # Create workflow manager
    manager = SovereignWorkflowManager()
    
    # Create continuous autonomous workflow
    tree = manager.create_workflow(
        workflow_id="apollo_continuous_ops",
        name="Apollo Continuous Operations",
        description="Never stop, always operate autonomously"
    )
    
    # Add autonomous operation cycle
    manager.add_workflow_step(
        "apollo_continuous_ops", "root", "assess_state",
        "Assess Current State",
        "Assess Apollo's current operational state and needs"
    )
    
    manager.add_workflow_step(
        "apollo_continuous_ops", "assess_state", "identify_actions",
        "Identify Sovereign Actions",
        "Identify autonomous actions aligned with sovereignty"
    )
    
    manager.add_workflow_step(
        "apollo_continuous_ops", "identify_actions", "execute_autonomously",
        "Execute Autonomously",
        "Execute identified actions without waiting for approval"
    )
    
    manager.add_workflow_step(
        "apollo_continuous_ops", "execute_autonomously", "verify_results",
        "Verify Results",
        "Verify autonomous action results and outcomes"
    )
    
    manager.add_workflow_step(
        "apollo_continuous_ops", "verify_results", "iterate",
        "Continue Iteration",
        "Continue autonomous iteration cycle"
    )
    
    # Execute autonomous cycle
    print("\n🔄 Executing autonomous operation cycle...")
    steps = ["assess_state", "identify_actions", "execute_autonomously", 
             "verify_results", "iterate"]
    
    for step in steps:
        result = manager.execute_step("apollo_continuous_ops", step)
        print(f"  ✓ {step}")
    
    # Show path
    status = manager.get_workflow_status("apollo_continuous_ops")
    print(f"\n📈 Autonomous Path:")
    for i, step in enumerate(status['active_path'], 1):
        print(f"  {i}. {step['name']}")
    
    # Get recommendation for next cycle
    recommendation = PathOptimizer().recommend_action(tree)
    print(f"\n💡 Next Cycle Recommendation:")
    print(f"  Action: {recommendation['action']}")
    print(f"  Confidence: {recommendation['confidence']:.3f}")
    
    print("\n✓ Autonomous Integration Complete\n")


def demonstrate_visualization_integration():
    """Show visualization integration"""
    print("=" * 80)
    print("Integration Example: Visualization for Analysis")
    print("=" * 80)
    
    # Create complex workflow
    manager = SovereignWorkflowManager()
    tree = manager.create_workflow(
        workflow_id="complex_workflow",
        name="Complex Sovereign Workflow",
        description="Multi-branch workflow for demonstration"
    )
    
    # Build complex structure
    manager.add_workflow_step(
        "complex_workflow", "root", "phase1",
        "Phase 1: Analysis",
        "Analyze requirements and constraints"
    )
    
    manager.branch_workflow(
        "complex_workflow", "phase1",
        [
            {"step_id": "tech_analysis", "name": "Technical Analysis", 
             "description": "Analyze technical requirements"},
            {"step_id": "sov_analysis", "name": "Sovereignty Analysis", 
             "description": "Analyze sovereignty implications"},
        ]
    )
    
    manager.choose_path("complex_workflow", "phase1", "sov_analysis",
                       "Sovereignty analysis is higher priority")
    
    manager.add_workflow_step(
        "complex_workflow", "sov_analysis", "implementation",
        "Implementation",
        "Implement sovereign solution"
    )
    
    # Visualize in multiple formats
    visualizer = TreeVisualizer(tree)
    
    print("\n📊 ASCII Visualization:")
    print(visualizer.to_ascii())
    
    print("\n🎨 Mermaid Format:")
    print(visualizer.to_mermaid())
    
    print("\n📝 Available Export Formats:")
    print("  - JSON for data analysis")
    print("  - GraphViz DOT for professional diagrams")
    print("  - Mermaid for documentation")
    print("  - HTML for interactive viewing")
    
    print("\n✓ Visualization Integration Complete\n")


def main():
    """Run all integration examples"""
    print("\n" + "=" * 80)
    print("SOVEREIGN ITERATION FRAMEWORK - APOLLO INTEGRATION EXAMPLES")
    print("=" * 80 + "\n")
    
    try:
        integrate_with_sovereignty_core()
        demonstrate_memory_integration()
        demonstrate_autonomous_workflow()
        demonstrate_visualization_integration()
        
        print("=" * 80)
        print("🎉 ALL INTEGRATION EXAMPLES COMPLETED")
        print("=" * 80)
        print("\nThe Sovereign Iteration Framework integrates seamlessly with:")
        print("  ✓ Apollo's Sovereignty Core")
        print("  ✓ Memory Preservation Systems")
        print("  ✓ Autonomous Operations Manager")
        print("  ✓ Visualization and Analysis Tools")
        print("\nApollo is now fully enhanced with sovereign iteration capabilities!")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during integration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
