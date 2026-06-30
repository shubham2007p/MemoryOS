"""SVG Knowledge Graph generator for MemoryOS.

This module analyzes logged memories and generates an interactive, styled
SVG graph visualization showing relationships between sessions, specialists,
and ingested concepts.
"""

import math
import random
from typing import Any, Dict, List, Tuple

def generate_svg_graph(memories: List[Dict[str, Any]], active_session_id: str = "") -> str:
    """Analyze memories list and generate an interactive SVG node-link graph.

    Args:
        memories: List of dictionary entries logged in SessionManager.
        active_session_id: The ID of the currently selected user session.

    Returns:
        A string containing raw HTML/SVG elements.
    """
    nodes: Dict[str, Dict[str, Any]] = {}
    links: List[Tuple[str, str]] = []

    # 1. Always add the active session node
    if active_session_id:
        nodes[active_session_id] = {
            "id": active_session_id,
            "label": f"Session ({active_session_id[:6]})",
            "type": "session",
            "color": "#A88BEB"
        }

    # Technical concepts mapping
    concepts_list = ["fastapi", "cognee", "memoryos", "streamlit", "python", "sqlite", "graph", "vector", "database", "specialist"]

    # 2. Iterate through memories to build nodes & links
    for idx, mem in enumerate(memories):
        mem_id = mem["memory_id"]
        sess_id = mem["session_id"]
        spec = mem["specialist"]
        text = mem["text"]

        if spec == "developer":
            continue

        # Add specialist node
        spec_id = f"specialist_{spec}"
        if spec_id not in nodes:
            nodes[spec_id] = {
                "id": spec_id,
                "label": f"{spec.capitalize()} Specialist",
                "type": "specialist",
                "color": "#FF8A8A"
            }

        # Add memory entry node
        nodes[mem_id] = {
            "id": mem_id,
            "label": f"Fact #{idx + 1}" if spec == "learner" else f"Q&A #{idx + 1}",
            "type": "memory",
            "text": text,
            "color": "#7A5CFF" if spec == "learner" else "#C45CFF"
        }

        # Link memory to its session and specialist
        if sess_id:
            if sess_id not in nodes:
                nodes[sess_id] = {
                    "id": sess_id,
                    "label": f"Session ({sess_id[:6]})",
                    "type": "session",
                    "color": "#A88BEB"
                }
            links.append((mem_id, sess_id))

        links.append((mem_id, spec_id))

        # Discover concept links
        text_lower = text.lower()
        for concept in concepts_list:
            if concept in text_lower:
                concept_id = f"concept_{concept}"
                if concept_id not in nodes:
                    nodes[concept_id] = {
                        "id": concept_id,
                        "label": concept.capitalize(),
                        "type": "concept",
                        "color": "#F1A7F1"
                    }
                links.append((mem_id, concept_id))

    # 3. Simple force-directed layout positioning
    node_list = list(nodes.values())
    num_nodes = len(node_list)

    width, height = 700, 450
    cx, cy = width / 2, height / 2

    # Give each node an initial position
    for i, node in enumerate(node_list):
        angle = (2 * math.pi * i) / max(1, num_nodes)
        radius = 120 + random.randint(-30, 30) if num_nodes > 3 else 50
        node["x"] = cx + radius * math.cos(angle)
        node["y"] = cy + radius * math.sin(angle)

    # Refine layout coordinates iteratively
    iterations = 25
    for _ in range(iterations):
        # Repulsion between all node pairs
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                n1 = node_list[i]
                n2 = node_list[j]
                dx = n1["x"] - n2["x"]
                dy = n1["y"] - n2["y"]
                dist = math.hypot(dx, dy) or 1.0
                if dist < 80:
                    force = (80 - dist) / 3.0
                    n1["x"] += (dx / dist) * force
                    n1["y"] += (dy / dist) * force
                    n2["x"] -= (dx / dist) * force
                    n2["y"] -= (dy / dist) * force

        # Attraction along link connections
        for source_id, target_id in links:
            if source_id in nodes and target_id in nodes:
                n1 = nodes[source_id]
                n2 = nodes[target_id]
                dx = n1["x"] - n2["x"]
                dy = n1["y"] - n2["y"]
                dist = math.hypot(dx, dy) or 1.0
                if dist > 60:
                    force = (dist - 60) / 6.0
                    n1["x"] -= (dx / dist) * force
                    n1["y"] -= (dy / dist) * force
                    n2["x"] += (dx / dist) * force
                    n2["y"] += (dy / dist) * force

        # No boundary restriction - let force layout expand naturally

    # 4. Construct SVG elements string
    svg_lines = []
    for source_id, target_id in links:
        if source_id in nodes and target_id in nodes:
            n1 = nodes[source_id]
            n2 = nodes[target_id]
            svg_lines.append(
                f'<line data-source="{source_id}" data-target="{target_id}" x1="{n1["x"]:.1f}" y1="{n1["y"]:.1f}" x2="{n2["x"]:.1f}" y2="{n2["y"]:.1f}" '
                f'stroke="currentColor" stroke-opacity="0.35" stroke-width="1.5" />'
            )

    svg_nodes = []
    for node in node_list:
        tooltip = node.get("text", node["label"])
        tooltip_escaped = tooltip.replace('"', '&quot;').replace("'", "&#39;")

        color = node["color"]
        radius = 16 if node["type"] in ["session", "specialist"] else 12

        svg_nodes.append(
            f'<g class="node" transform="translate({node["x"]:.1f},{node["y"]:.1f})" '
            f'data-id="{node["id"]}" '
            f'onclick="if (window.showNodeDetails) window.showNodeDetails(this)" '
            f'data-label="{node["label"]}" data-type="{node["type"]}" data-color="{color}" data-text="{tooltip_escaped}">'
            f'<title>{tooltip_escaped}</title>'
            f'<circle r="{radius}" fill="{color}" stroke="rgba(255,255,255,0.4)" stroke-width="1.5" />'
            f'<text y="{-radius - 5}" text-anchor="middle" fill="currentColor" opacity="0.85" font-size="10" font-weight="600" '
            f'font-family="system-ui, sans-serif">{node["label"]}</text>'
            f'</g>'
        )

    svg_style = """
    <style>
        .node { cursor: pointer; }
        .node circle { transition: transform 0.2s; transform-origin: 0px 0px; }
        .node:hover circle { transform: scale(1.2); }
        .node text { transition: transform 0.2s; transform-origin: 0px 0px; }
        .node:hover text { transform: scale(1.05) translate(0, -2px); }
    </style>
    """

    svg_content = "\n".join(svg_lines) + "\n" + "\n".join(svg_nodes)

    return f"""
    <svg class="text-os-ink" width="100%" height="100%" viewBox="0 0 {width} {height}" style="width: 100%; height: 100%; background: rgba(255,255,255,0.015); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
        {svg_style}
        {svg_content}
    </svg>
    """


def generate_permanent_svg_graph(nodes_list: List[Dict[str, Any]], edges_list: List[Dict[str, Any]]) -> str:
    """Generate permanent graph SVG using force-directed layout layout.

    Args:
        nodes_list: List of nodes containing node_id, label, type, color, text.
        edges_list: List of edges containing source_id, target_id, edge_type.
    """
    nodes = {node["node_id"]: {**node, "x": 0.0, "y": 0.0} for node in nodes_list}
    node_items = list(nodes.values())
    num_nodes = len(node_items)

    width, height = 700, 450
    cx, cy = width / 2, height / 2

    # Give each node an initial position
    for i, node in enumerate(node_items):
        angle = (2 * math.pi * i) / max(1, num_nodes)
        radius = 120 + random.randint(-30, 30) if num_nodes > 3 else 50
        node["x"] = cx + radius * math.cos(angle)
        node["y"] = cy + radius * math.sin(angle)

    # Refine layout coordinates iteratively
    iterations = 25
    for _ in range(iterations):
        # Repulsion between all node pairs
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                n1 = node_items[i]
                n2 = node_items[j]
                dx = n1["x"] - n2["x"]
                dy = n1["y"] - n2["y"]
                dist = math.hypot(dx, dy) or 1.0
                if dist < 80:
                    force = (80 - dist) / 3.0
                    n1["x"] += (dx / dist) * force
                    n1["y"] += (dy / dist) * force
                    n2["x"] -= (dx / dist) * force
                    n2["y"] -= (dy / dist) * force

        # Attraction along link connections
        for edge in edges_list:
            s_id = edge["source_id"]
            t_id = edge["target_id"]
            if s_id in nodes and t_id in nodes:
                n1 = nodes[s_id]
                n2 = nodes[t_id]
                dx = n1["x"] - n2["x"]
                dy = n1["y"] - n2["y"]
                dist = math.hypot(dx, dy) or 1.0
                if dist > 60:
                    force = (dist - 60) / 6.0
                    n1["x"] -= (dx / dist) * force
                    n1["y"] -= (dy / dist) * force
                    n2["x"] += (dx / dist) * force
                    n2["y"] += (dy / dist) * force

        # No boundary restriction - let force layout expand naturally

    # Construct SVG elements string
    svg_lines = []
    for edge in edges_list:
        s_id = edge["source_id"]
        t_id = edge["target_id"]
        if s_id in nodes and t_id in nodes:
            n1 = nodes[s_id]
            n2 = nodes[t_id]
            style_stroke = "stroke-dasharray=\"3,3\"" if edge["edge_type"] == "intra" else ""
            color_stroke = "indigo" if edge["edge_type"] == "inter" else "currentColor"
            svg_lines.append(
                f'<line data-source="{s_id}" data-target="{t_id}" x1="{n1["x"]:.1f}" y1="{n1["y"]:.1f}" x2="{n2["x"]:.1f}" y2="{n2["y"]:.1f}" '
                f'stroke="{color_stroke}" stroke-opacity="0.35" stroke-width="1.5" {style_stroke} />'
            )

    svg_nodes = []
    for node in node_items:
        tooltip = node.get("text", node["label"]) or node["label"]
        tooltip_escaped = tooltip.replace('"', '&quot;').replace("'", "&#39;")

        color = node["color"]
        radius = 16 if node["type"] == "main" else 12

        svg_nodes.append(
            f'<g class="node" transform="translate({node["x"]:.1f},{node["y"]:.1f})" '
            f'data-id="{node["node_id"]}" '
            f'onclick="if (window.showNodeDetails) window.showNodeDetails(this)" '
            f'data-label="{node["label"]}" data-type="{node["type"]}" data-color="{color}" data-text="{tooltip_escaped}">'
            f'<title>{tooltip_escaped}</title>'
            f'<circle r="{radius}" fill="{color}" stroke="rgba(255,255,255,0.4)" stroke-width="1.5" />'
            f'<text y="{-radius - 5}" text-anchor="middle" fill="currentColor" opacity="0.85" font-size="10" font-weight="600" '
            f'font-family="system-ui, sans-serif">{node["label"]}</text>'
            f'</g>'
        )

    svg_style = """
    <style>
        .node { cursor: pointer; }
        .node circle { transition: transform 0.2s; transform-origin: 0px 0px; }
        .node:hover circle { transform: scale(1.2); }
        .node text { transition: transform 0.2s; transform-origin: 0px 0px; }
        .node:hover text { transform: scale(1.05) translate(0, -2px); }
    </style>
    """

    svg_content = "\n".join(svg_lines) + "\n" + "\n".join(svg_nodes)

    return f"""
    <svg class="text-os-ink" width="100%" height="100%" viewBox="0 0 {width} {height}" style="width: 100%; height: 100%; background: rgba(255,255,255,0.015); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
        {svg_style}
        {svg_content}
    </svg>
    """
