"""
Sovereign Tree Visualizer
Provides visualization and interactive navigation for sovereign iteration trees.
Supports export to various formats for analysis and presentation.
"""

from typing import Dict, List, Optional, Any, TextIO
from pathlib import Path
import json

from core.sovereign_iteration_framework import (
    IterationTree, IterationNode, NodeType, NodeStatus
)


class TreeVisualizer:
    """
    Visualizes iteration trees in various formats.
    """
    
    def __init__(self, tree: IterationTree):
        self.tree = tree
    
    def to_ascii(self, max_depth: Optional[int] = None) -> str:
        """
        Generate ASCII tree visualization.
        
        Args:
            max_depth: Maximum depth to visualize (None for unlimited)
        
        Returns:
            ASCII art representation of the tree
        """
        if self.tree.root_id is None:
            return "Empty tree"
        
        lines = []
        
        def render_node(node_id: str, prefix: str = "", is_last: bool = True,
                       depth: int = 0) -> None:
            if max_depth is not None and depth > max_depth:
                return
            
            node = self.tree.get_node(node_id)
            if node is None:
                return
            
            # Choose connector
            connector = "└── " if is_last else "├── "
            
            # Status indicator
            status_symbol = {
                NodeStatus.PENDING: "○",
                NodeStatus.ACTIVE: "●",
                NodeStatus.COMPLETED: "✓",
                NodeStatus.ABANDONED: "✗"
            }.get(node.status, "?")
            
            # Type indicator
            type_symbol = {
                NodeType.ACTION: "A",
                NodeType.STATE: "S",
                NodeType.DECISION: "D",
                NodeType.MILESTONE: "M"
            }.get(node.node_type, "?")
            
            # Build line
            line = f"{prefix}{connector}[{status_symbol}][{type_symbol}] {node.name}"
            if node.resonance_score > 0:
                line += f" (R:{node.resonance_score:.2f})"
            
            lines.append(line)
            
            # Render children
            children_ids = node.children_ids
            for i, child_id in enumerate(children_ids):
                is_last_child = (i == len(children_ids) - 1)
                extension = "    " if is_last else "│   "
                render_node(child_id, prefix + extension, is_last_child, depth + 1)
        
        render_node(self.tree.root_id)
        return "\n".join(lines)
    
    def to_json(self, pretty: bool = True) -> str:
        """
        Export tree to JSON format.
        
        Args:
            pretty: Whether to format with indentation
        
        Returns:
            JSON string representation
        """
        tree_dict = self.tree.to_dict()
        indent = 2 if pretty else None
        return json.dumps(tree_dict, indent=indent)
    
    def to_graphviz(self) -> str:
        """
        Generate GraphViz DOT format for visualization.
        Can be rendered with tools like Graphviz or online viewers.
        
        Returns:
            DOT format string
        """
        lines = ["digraph SovereignIterationTree {"]
        lines.append("    rankdir=TB;")
        lines.append("    node [shape=box, style=rounded];")
        lines.append("")
        
        # Define nodes
        for node_id, node in self.tree.nodes.items():
            # Node color based on status
            color = {
                NodeStatus.PENDING: "lightgray",
                NodeStatus.ACTIVE: "lightblue",
                NodeStatus.COMPLETED: "lightgreen",
                NodeStatus.ABANDONED: "lightcoral"
            }.get(node.status, "white")
            
            # Node shape based on type
            shape = {
                NodeType.ACTION: "box",
                NodeType.STATE: "ellipse",
                NodeType.DECISION: "diamond",
                NodeType.MILESTONE: "doubleoctagon"
            }.get(node.node_type, "box")
            
            # Build label
            label = f"{node.name}\\n"
            label += f"Type: {node.node_type.value}\\n"
            label += f"Status: {node.status.value}\\n"
            if node.resonance_score > 0:
                label += f"Resonance: {node.resonance_score:.2f}"
            
            lines.append(
                f'    "{node_id}" [label="{label}", '
                f'fillcolor="{color}", style=filled, shape={shape}];'
            )
        
        lines.append("")
        
        # Define edges
        for node_id, node in self.tree.nodes.items():
            for child_id in node.children_ids:
                # Edge style based on active path
                style = "solid"
                width = "1.0"
                color = "black"
                
                active_path_ids = [n.node_id for n in self.tree.get_active_path()]
                if node_id in active_path_ids and child_id in active_path_ids:
                    style = "bold"
                    width = "2.0"
                    color = "blue"
                
                lines.append(
                    f'    "{node_id}" -> "{child_id}" '
                    f'[style={style}, penwidth={width}, color={color}];'
                )
        
        lines.append("}")
        return "\n".join(lines)
    
    def to_mermaid(self) -> str:
        """
        Generate Mermaid diagram format for visualization.
        Can be rendered in Markdown viewers and documentation.
        
        Returns:
            Mermaid format string
        """
        lines = ["graph TD"]
        
        # Define nodes
        for node_id, node in self.tree.nodes.items():
            # Node style based on status
            status_symbol = {
                NodeStatus.PENDING: "○",
                NodeStatus.ACTIVE: "●",
                NodeStatus.COMPLETED: "✓",
                NodeStatus.ABANDONED: "✗"
            }.get(node.status, "?")
            
            # Bracket style based on type
            if node.node_type == NodeType.DECISION:
                brackets = ("{", "}")
            elif node.node_type == NodeType.MILESTONE:
                brackets = ("([", "])")
            elif node.node_type == NodeType.STATE:
                brackets = ("(", ")")
            else:
                brackets = ("[", "]")
            
            label = f"{status_symbol} {node.name}"
            
            lines.append(f'    {node_id}{brackets[0]}"{label}"{brackets[1]}')
        
        # Define edges
        for node_id, node in self.tree.nodes.items():
            for child_id in node.children_ids:
                lines.append(f'    {node_id} --> {child_id}')
        
        # Style active path
        active_path_ids = [n.node_id for n in self.tree.get_active_path()]
        if active_path_ids:
            style_list = ",".join(active_path_ids)
            lines.append(f'    style {style_list} fill:#90caf9')
        
        return "\n".join(lines)
    
    def export_html(self, output_path: Path, include_interactive: bool = True) -> None:
        """
        Export tree as interactive HTML visualization.
        
        Args:
            output_path: Path to save HTML file
            include_interactive: Whether to include JavaScript for interactivity
        """
        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "    <meta charset='utf-8'>",
            "    <title>Sovereign Iteration Tree</title>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; margin: 20px; }",
            "        h1 { color: #333; }",
            "        .tree-container { margin: 20px 0; }",
            "        .node { margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }",
            "        .node-active { background-color: #e3f2fd; }",
            "        .node-completed { background-color: #e8f5e9; }",
            "        .node-pending { background-color: #f5f5f5; }",
            "        .node-abandoned { background-color: #ffebee; }",
            "        .node-header { font-weight: bold; margin-bottom: 5px; }",
            "        .node-meta { font-size: 0.9em; color: #666; }",
            "        .children { margin-left: 30px; }",
            "        .stats { background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px; }",
            "    </style>",
            "</head>",
            "<body>",
            f"    <h1>Sovereign Iteration Tree: {self.tree.tree_id}</h1>",
        ]
        
        # Add statistics
        stats = self.tree.get_statistics()
        html_parts.append("    <div class='stats'>")
        html_parts.append("        <h2>Statistics</h2>")
        html_parts.append(f"        <p>Total Nodes: {stats['total_nodes']}</p>")
        html_parts.append(f"        <p>Active Node: {stats['active_node_id']}</p>")
        html_parts.append("        <p>Nodes by Status:</p>")
        html_parts.append("        <ul>")
        for status, count in stats['nodes_by_status'].items():
            html_parts.append(f"            <li>{status}: {count}</li>")
        html_parts.append("        </ul>")
        html_parts.append("    </div>")
        
        # Add tree visualization
        html_parts.append("    <div class='tree-container'>")
        html_parts.append("        <h2>Tree Structure</h2>")
        
        def render_node_html(node_id: str) -> List[str]:
            node = self.tree.get_node(node_id)
            if node is None:
                return []
            
            status_class = f"node-{node.status.value}"
            parts = [f"        <div class='node {status_class}' id='node-{node_id}'>"]
            parts.append(f"            <div class='node-header'>{node.name}</div>")
            parts.append(f"            <div class='node-meta'>")
            parts.append(f"                Type: {node.node_type.value} | ")
            parts.append(f"                Status: {node.status.value} | ")
            parts.append(f"                Resonance: {node.resonance_score:.2f}")
            parts.append(f"            </div>")
            parts.append(f"            <div>{node.description}</div>")
            
            if node.children_ids:
                parts.append("            <div class='children'>")
                for child_id in node.children_ids:
                    parts.extend(render_node_html(child_id))
                parts.append("            </div>")
            
            parts.append("        </div>")
            return parts
        
        if self.tree.root_id:
            html_parts.extend(render_node_html(self.tree.root_id))
        
        html_parts.append("    </div>")
        
        # Add interactive features
        if include_interactive:
            html_parts.extend([
                "    <script>",
                "        // Add click handlers for node inspection",
                "        document.querySelectorAll('.node').forEach(node => {",
                "            node.style.cursor = 'pointer';",
                "            node.addEventListener('click', (e) => {",
                "                e.stopPropagation();",
                "                node.classList.toggle('highlighted');",
                "            });",
                "        });",
                "    </script>",
            ])
        
        html_parts.extend([
            "</body>",
            "</html>"
        ])
        
        with open(output_path, 'w') as f:
            f.write("\n".join(html_parts))


class InteractiveNavigator:
    """
    Provides interactive navigation capabilities for iteration trees.
    """
    
    def __init__(self, tree: IterationTree):
        self.tree = tree
        self.current_node_id = tree.active_node_id or tree.root_id
    
    def move_to_node(self, node_id: str) -> Optional[IterationNode]:
        """Move to a specific node"""
        node = self.tree.get_node(node_id)
        if node is not None:
            self.current_node_id = node_id
        return node
    
    def move_to_parent(self) -> Optional[IterationNode]:
        """Move to parent of current node"""
        if self.current_node_id is None:
            return None
        
        node = self.tree.get_node(self.current_node_id)
        if node is None or node.parent_id is None:
            return None
        
        return self.move_to_node(node.parent_id)
    
    def move_to_child(self, index: int = 0) -> Optional[IterationNode]:
        """Move to nth child of current node"""
        if self.current_node_id is None:
            return None
        
        children = self.tree.get_children(self.current_node_id)
        if not children or index >= len(children):
            return None
        
        return self.move_to_node(children[index].node_id)
    
    def move_to_root(self) -> Optional[IterationNode]:
        """Move to root node"""
        if self.tree.root_id is None:
            return None
        return self.move_to_node(self.tree.root_id)
    
    def get_current_context(self) -> Dict[str, Any]:
        """Get context information about current position"""
        if self.current_node_id is None:
            return {"error": "No current node"}
        
        node = self.tree.get_node(self.current_node_id)
        if node is None:
            return {"error": "Current node not found"}
        
        children = self.tree.get_children(self.current_node_id)
        path = self.tree.get_path_to_root(self.current_node_id)
        
        return {
            "current_node": {
                "id": node.node_id,
                "name": node.name,
                "description": node.description,
                "type": node.node_type.value,
                "status": node.status.value,
                "resonance": node.resonance_score
            },
            "parent_id": node.parent_id,
            "children": [
                {"id": c.node_id, "name": c.name, "status": c.status.value}
                for c in children
            ],
            "path_from_root": [
                {"id": n.node_id, "name": n.name}
                for n in path
            ],
            "depth": len(path) - 1
        }
    
    def find_nodes(self, query: str, search_field: str = "name") -> List[IterationNode]:
        """
        Search for nodes by name, description, or metadata.
        
        Args:
            query: Search query string
            search_field: Field to search in ('name', 'description', 'metadata')
        
        Returns:
            List of matching nodes
        """
        query_lower = query.lower()
        results = []
        
        for node in self.tree.nodes.values():
            if search_field == "name" and query_lower in node.name.lower():
                results.append(node)
            elif search_field == "description" and query_lower in node.description.lower():
                results.append(node)
            elif search_field == "metadata":
                metadata_str = json.dumps(node.metadata).lower()
                if query_lower in metadata_str:
                    results.append(node)
        
        return results
