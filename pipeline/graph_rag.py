"""
GraphRAG knowledge graph: builds and queries a NetworkX graph
from business intelligence data (businesses → skills → email signals → career pages).
"""

from __future__ import annotations
from typing import Any
import networkx as nx


def build_graph(businesses: list[dict]) -> nx.DiGraph:
    """
    Build a directed knowledge graph from processed business data.

    Node types:
      - business  (name, address, rating)
      - skill     (skill_name, skill_id)
      - email     (address, label, confidence)
      - career    (url, confidence)
      - group     (business group name)

    Edges:
      - business → group     (belongs_to)
      - business → skill     (requires_skill)
      - business → email     (has_email)
      - business → career    (has_career_page)
      - email    → label     (classified_as)
    """
    G = nx.DiGraph()

    for biz in businesses:
        biz_id = f"biz::{biz['name']}"
        G.add_node(
            biz_id,
            node_type="business",
            label=biz["name"],
            address=biz.get("address", ""),
            rating=biz.get("rating", 0),
            website=biz.get("website", ""),
        )

        # Group node
        group = biz.get("business_group", "Unknown")
        group_id = f"group::{group}"
        if not G.has_node(group_id):
            G.add_node(group_id, node_type="group", label=_pretty_group(group))
        G.add_edge(biz_id, group_id, relation="belongs_to")

        # Skill nodes
        for skill in biz.get("skills", []):
            skill_id = f"skill::{skill['skill_id']}"
            if not G.has_node(skill_id):
                G.add_node(
                    skill_id,
                    node_type="skill",
                    label=skill["skill_name"].split(">")[-1].strip(),
                    full_name=skill["skill_name"],
                    skill_id=skill["skill_id"],
                )
            G.add_edge(biz_id, skill_id, relation="requires_skill", tag=skill.get("tag", ""))

        # Email nodes
        for ec in biz.get("email_classifications", []):
            email_node_id = f"email::{ec['email']}"
            G.add_node(
                email_node_id,
                node_type="email",
                label=ec["email"],
                email_label=ec["label"],
                confidence=ec["confidence"],
            )
            G.add_edge(biz_id, email_node_id, relation="has_email")

            label_node_id = f"label::{ec['label']}"
            if not G.has_node(label_node_id):
                G.add_node(label_node_id, node_type="signal_label", label=ec["label"])
            G.add_edge(email_node_id, label_node_id, relation="classified_as", confidence=ec["confidence"])

        # Career page node
        if biz.get("has_career_page"):
            career_url = biz.get("career_page_url", "")
            career_id = f"career::{biz['name']}"
            G.add_node(
                career_id,
                node_type="career",
                label=f"Career Page",
                url=career_url,
                confidence=biz.get("career_detection", {}).get("confidence", 0),
            )
            G.add_edge(biz_id, career_id, relation="has_career_page")

    return G


def _pretty_group(group: str) -> str:
    return group.replace("_", " ").replace("and", "&").title()


def graph_stats(G: nx.DiGraph) -> dict:
    node_types = {}
    for _, data in G.nodes(data=True):
        t = data.get("node_type", "unknown")
        node_types[t] = node_types.get(t, 0) + 1

    return {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "node_types": node_types,
        "connected_components": nx.number_weakly_connected_components(G),
    }


def get_business_subgraph(G: nx.DiGraph, business_name: str) -> nx.DiGraph:
    """Return the 2-hop neighborhood subgraph for a given business."""
    biz_id = f"biz::{business_name}"
    if biz_id not in G:
        return nx.DiGraph()
    neighbors = set(nx.single_source_shortest_path_length(G, biz_id, cutoff=2).keys())
    return G.subgraph(neighbors).copy()


def query_hr_signals(G: nx.DiGraph) -> list[dict]:
    """Return all HR email signals from the graph."""
    results = []
    for node_id, data in G.nodes(data=True):
        if data.get("node_type") == "email" and data.get("email_label") == "HR":
            preds = list(G.predecessors(node_id))
            biz_name = preds[0].replace("biz::", "") if preds else "Unknown"
            results.append({
                "business": biz_name,
                "email": data["label"],
                "confidence": data.get("confidence", 0),
            })
    return sorted(results, key=lambda x: x["confidence"], reverse=True)


def to_plotly_data(G: nx.DiGraph) -> dict[str, Any]:
    """
    Convert graph to Plotly scatter trace data for visualization.
    Uses spring layout for positioning.
    """
    if G.number_of_nodes() == 0:
        return {"node_x": [], "node_y": [], "node_text": [], "node_color": [], "edge_x": [], "edge_y": []}

    try:
        pos = nx.kamada_kawai_layout(G)
    except Exception:
        pos = nx.circular_layout(G)

    COLOR_MAP = {
        "business": "#4F8EF7",
        "group": "#F7994F",
        "skill": "#4FF7A0",
        "email": "#F74F4F",
        "career": "#BF4FF7",
        "signal_label": "#F7E44F",
        "unknown": "#AAAAAA",
    }

    node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
    for node_id, data in G.nodes(data=True):
        x, y = pos[node_id]
        node_x.append(x)
        node_y.append(y)
        node_text.append(data.get("label", node_id))
        node_color.append(COLOR_MAP.get(data.get("node_type", "unknown"), "#AAAAAA"))
        node_size.append(20 if data.get("node_type") == "business" else 12)

    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    return {
        "node_x": node_x,
        "node_y": node_y,
        "node_text": node_text,
        "node_color": node_color,
        "node_size": node_size,
        "edge_x": edge_x,
        "edge_y": edge_y,
    }
