from orchestrator.graph_viewer import generate_svg_graph

def test_generate_svg_graph_empty():
    """Verify that generating an SVG graph from an empty list returns valid basic SVG tags."""
    svg = generate_svg_graph([])
    assert "<svg" in svg
    assert "</svg>" in svg

def test_generate_svg_graph_with_data():
    """Verify that SVG incorporates session and concept nodes from input list."""
    memories = [
        {
            "memory_id": "mem-1",
            "session_id": "session-1",
            "specialist": "learner",
            "text": "MemoryOS is built using FastAPI.",
            "metadata": {}
        }
    ]
    svg = generate_svg_graph(memories, active_session_id="session-1")
    assert "<svg" in svg
    assert "Session" in svg
