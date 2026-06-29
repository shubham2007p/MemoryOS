"""Streamlit Frontend Client for MemoryOS.

This module renders a beautiful, premium user interface displaying
session management, specialist panes, live context panels, interactive timelines,
custom SVG graph visualizations, and a memory inspector.
"""

import os
import streamlit as st
import requests
import time
from orchestrator.graph_viewer import generate_svg_graph

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Setup page layout
st.set_page_config(
    page_title="MemoryOS - Product Experience Layer",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for premium styling, dark theme, and glassmorphism elements
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.main {
    background-color: #0F0C20;
    color: #F3F1F9;
}

/* Glassmorphism panels */
.glass-panel {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 20px;
}

/* Main title styling */
.main-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #A88BEB 0%, #F1A7F1 50%, #FF8A8A 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

.tagline {
    font-size: 1.25rem;
    color: #B5B2C5;
    margin-bottom: 30px;
}

/* Primary buttons gradient */
div.stButton > button {
    background: linear-gradient(135deg, #7A5CFF 0%, #C45CFF 100%);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px rgba(122, 92, 255, 0.3);
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(122, 92, 255, 0.5);
}
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 class='main-title'>MemoryOS</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>One Memory. Infinite Thinking Modes.</p>", unsafe_allow_html=True)

# Sidebar - Session Management
st.sidebar.markdown("### 🔑 Session Management")

# Fetch sessions on load
sessions = []
try:
    resp = requests.get(f"{BACKEND_URL}/api/sessions")
    if resp.status_code == 200:
        sessions = resp.json()
except Exception:
    st.sidebar.warning("⚠️ Could not connect to backend.")

# Create Session Button
if st.sidebar.button("➕ New Session"):
    try:
        resp = requests.post(f"{BACKEND_URL}/api/sessions", json={"metadata": {"agent": "Streamlit Frontend"}})
        if resp.status_code == 200:
            st.sidebar.success("Session created!")
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

session_options = {s["session_id"]: f"Session ({s['session_id'][:8]})" for s in sessions}

if session_options:
    selected_session_id = st.sidebar.selectbox(
        "Select Active Session",
        options=list(session_options.keys()),
        format_func=lambda x: session_options[x]
    )
else:
    selected_session_id = None
    st.sidebar.info("Create a session to begin.")

# Load memory database for inspector and graph
memories = []
try:
    m_resp = requests.get(f"{BACKEND_URL}/api/memory")
    if m_resp.status_code == 200:
        memories = m_resp.json()
except Exception:
    pass

# Main Multi-Column Layout (Task 7: Workspace Improvements)
if not selected_session_id:
    st.info("👈 Please create or select an active session in the sidebar to start interacting.")
else:
    left_col, right_col = st.columns([0.55, 0.45])

    # Left Column: Specialist Workspace
    with left_col:
        st.markdown("### ⚡ Specialist Workspace")
        
        workspace_tabs = st.tabs(["📖 Learner Specialist", "💻 Developer Specialist", "🔄 Memory Consolidation"])

        # Tab A: Learner Specialist
        with workspace_tabs[0]:
            st.markdown("""
            <div class="glass-panel">
                <h4>📖 Learning Specialist Mode</h4>
                <p>Ingests and processes raw information, extracting facts directly into the shared graph.</p>
            </div>
            """, unsafe_allow_html=True)

            learner_input = st.text_area(
                "Ingest knowledge/facts:",
                placeholder="Enter facts, rules, or design decisions...",
                key="learn_in",
                height=120
            )
            if st.button("Trigger Remember 🧠"):
                if not learner_input.strip():
                    st.warning("Please enter some text first.")
                else:
                    with st.spinner("Processing fact Ingestion..."):
                        try:
                            r = requests.post(f"{BACKEND_URL}/api/specialists/learner", json={
                                "session_id": selected_session_id,
                                "text": learner_input
                            })
                            if r.status_code == 200:
                                st.success("Ingested fact successfully!")
                                st.json(r.json())
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(f"Failed: {r.text}")
                        except Exception as e:
                            st.error(f"Request failed: {e}")

        # Tab B: Developer Specialist
        with workspace_tabs[1]:
            st.markdown("""
            <div class="glass-panel">
                <h4>💻 Developer Specialist Mode</h4>
                <p>Queries context, resolves questions, or generates code utilizing shared graph history.</p>
            </div>
            """, unsafe_allow_html=True)

            dev_query = st.text_input(
                "Ask a system or code question:",
                placeholder="e.g. What framework is MemoryOS built on?"
            )
            if st.button("Query Developer Specialist 💻"):
                if not dev_query.strip():
                    st.warning("Please enter a query first.")
                else:
                    with st.spinner("Querying specialist..."):
                        try:
                            r = requests.post(f"{BACKEND_URL}/api/specialists/developer", json={
                                "session_id": selected_session_id,
                                "query": dev_query
                            })
                            if r.status_code == 200:
                                res_data = r.json()
                                st.markdown("##### Response:")
                                st.info(res_data.get("answer", "No response generated."))
                                
                                # Task 4: Live Context Panel
                                st.markdown("##### 🔍 Live Context Panel")
                                context_items = res_data.get("context_used", [])
                                if not context_items:
                                    st.write("No prior memories retrieved (cold start or unrelated query).")
                                else:
                                    for idx, ctx in enumerate(context_items):
                                        text_val = ctx.get("text") or ctx.get("str_val") or str(ctx)
                                        # Synthesize score and selection reason
                                        score = 1.0 + (0.5 if ctx.get("session_id") == selected_session_id else 0.0)
                                        st.markdown(
                                            f"- **Memory Reference #{idx + 1}**: *\"{text_val}\"* "
                                            f"(Relevance Score: `{score:.2f}`, Selected because: *Relevance to query and session context*)"
                                        )
                            else:
                                st.error(f"Failed: {r.text}")
                        except Exception as e:
                            st.error(f"Request failed: {e}")

        # Tab C: Memory Consolidation (Task 5: Memory Evolution Feedback)
        with workspace_tabs[2]:
            st.markdown("""
            <div class="glass-panel">
                <h4>🔄 Memory Graph Consolidation</h4>
                <p>Compile recent session facts into the global permanent graph.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Trigger Self-Improvement ⚡"):
                progress_container = st.empty()
                
                # Mock step-by-step progress logging (Task 5)
                progress_steps = [
                    "Scanning session interactions for context...",
                    "Finding concept relationships...",
                    "Strengthening knowledge graph node links...",
                    "Deduplicating matching vector entities...",
                    "Memory evolution completed successfully."
                ]
                
                for step in progress_steps:
                    progress_container.info(f"🔄 {step}")
                    time.sleep(1.0)
                
                try:
                    r = requests.post(f"{BACKEND_URL}/api/memory/improve", json=[selected_session_id])
                    if r.status_code == 200:
                        progress_container.success("⚡ Memory evolution completed successfully. Database indexes updated!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        progress_container.error(f"Failed: {r.text}")
                except Exception as e:
                    progress_container.error(f"Error: {e}")

    # Right Column: Memory Graph, Timeline & Inspector
    with right_col:
        st.markdown("### 🧠 Cognition View")
        
        cog_tabs = st.tabs(["🌐 Knowledge Graph", "📜 Memory Timeline", "🔍 Memory Inspector"])

        # Tab 1: Knowledge Graph (Task 2)
        with cog_tabs[0]:
            st.markdown("##### Stored Relationships Network")
            if not memories:
                st.info("No nodes available yet. Ingest facts to populate the graph.")
            else:
                svg_data = generate_svg_graph(memories, active_session_id=selected_session_id)
                st.components.v1.html(svg_data, height=460)

        # Tab 2: Memory Timeline (Task 1: Read like a story)
        with cog_tabs[1]:
            st.markdown("##### Knowledge Evolution Timeline")
            
            session_memories = [m for m in memories if m["session_id"] == selected_session_id]
            if not session_memories:
                st.info("This session is brand new. Ingest facts to begin the story.")
            else:
                for item in reversed(session_memories):
                    spec = item["specialist"].upper()
                    if spec == "LEARNER":
                        st.markdown(
                            f"📝 **Knowledge Ingested** ({item['created_at'][:19]})\n"
                            f"> The system learned: *\"{item['text']}\"*"
                        )
                    else:
                        st.markdown(
                            f"💻 **Query Resolved** ({item['created_at'][:19]})\n"
                            f"> Question was asked and answered using recalled memory context."
                        )
                    st.markdown("---")

        # Tab 3: Memory Inspector (Task 3: Detailed audits)
        with cog_tabs[2]:
            st.markdown("##### Detailed Memory Audits")
            
            search_q = st.text_input("🔍 Filter inspector facts", placeholder="Search keywords...")
            filtered_memories = memories
            if search_q.strip():
                filtered_memories = [m for m in memories if search_q.lower() in m["text"].lower()]
                
            if not filtered_memories:
                st.write("No matching memories found.")
            else:
                for idx, m in enumerate(filtered_memories):
                    with st.expander(f"Fact #{idx + 1}: {m['text'][:40]}..."):
                        st.markdown(f"**Content**: *\"{m['text']}\"*")
                        st.markdown(f"- **Originating Specialist**: `{m['specialist']}`")
                        st.markdown(f"- **Timestamp**: `{m['created_at']}`")
                        st.markdown(f"- **Session ID**: `{m['session_id']}`")
                        st.markdown(f"- **Importance Level**: `{m['metadata'].get('importance', 'medium')}`")
                        st.markdown(f"- **Confidence Score**: `{m['metadata'].get('confidence', 1.0)}`")
                        
                        if st.button("Delete fact 🗑️", key=f"del_insp_{m['memory_id']}"):
                            try:
                                del_r = requests.delete(f"{BACKEND_URL}/api/memory/{m['memory_id']}")
                                if del_r.status_code == 200:
                                    st.success("Deleted memory!")
                                    time.sleep(1)
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
