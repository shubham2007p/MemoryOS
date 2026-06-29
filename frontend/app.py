"""Streamlit Frontend Client for MemoryOS.

This module renders a beautiful, premium user interface displaying
session management, a Learning Specialist pane, a Developer Specialist pane,
memory consolidation controls, and a complete memory inspector with search and deletion capabilities.
"""

import os
import streamlit as st
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Setup page layout
st.set_page_config(
    page_title="MemoryOS - One Memory, Infinite Thinking Modes",
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
    padding: 24px;
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
    padding: 12px 24px;
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

# Main Tabs Setup
tab1, tab2 = st.tabs(["⚡ Active Workspace", "📂 Memory Inspector"])

# Tab 1: Active Workspace
with tab1:
    if not selected_session_id:
        st.info("👈 Please create or select an active session in the sidebar to start interacting.")
    else:
        # Specialist Panels
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="glass-panel">
                <h3>📖 Learning Specialist</h3>
                <p>Ingests and processes raw information, extracting facts and concepts directly into the persistent Cognee Memory Graph.</p>
            </div>
            """, unsafe_allow_html=True)

            learner_input = st.text_area(
                "What would you like the system to learn?",
                placeholder="Enter facts, documentation, or rules...",
                key="learn_in",
                height=150
            )
            if st.button("Trigger Remember 🧠"):
                if not learner_input.strip():
                    st.warning("Please enter some text first.")
                else:
                    with st.spinner("Analyzing and ingesting facts into Cognee..."):
                        try:
                            r = requests.post(f"{BACKEND_URL}/api/specialists/learner", json={
                                "session_id": selected_session_id,
                                "text": learner_input
                            })
                            if r.status_code == 200:
                                res_data = r.json()
                                st.success("Ingestion complete!")
                                st.json(res_data)
                            else:
                                st.error(f"Failed to learn: {r.text}")
                        except Exception as e:
                            st.error(f"Backend request failed: {e}")

        with col2:
            st.markdown("""
            <div class="glass-panel">
                <h3>💻 Developer Specialist</h3>
                <p>Queries/recalls from the shared Cognee memory database and reasons using LLM thinking to answer questions or write code.</p>
            </div>
            """, unsafe_allow_html=True)

            dev_query = st.text_input(
                "Ask a question or request code generation",
                placeholder="e.g. What is MemoryOS built on?"
            )
            if st.button("Query Developer Specialist 💻"):
                if not dev_query.strip():
                    st.warning("Please enter a query first.")
                else:
                    with st.spinner("Recalling context and generating response..."):
                        try:
                            r = requests.post(f"{BACKEND_URL}/api/specialists/developer", json={
                                "session_id": selected_session_id,
                                "query": dev_query
                            })
                            if r.status_code == 200:
                                res_data = r.json()
                                st.markdown("#### Response:")
                                st.info(res_data.get("answer", "No answer generated."))
                                if "context_used" in res_data:
                                    with st.expander("Recalled Context details"):
                                        st.json(res_data["context_used"])
                            else:
                                st.error(f"Query failed: {r.text}")
                        except Exception as e:
                            st.error(f"Backend request failed: {e}")

        # Active Session history
        st.markdown("---")
        st.markdown("### 📜 Session Activity History")
        try:
            history_resp = requests.get(f"{BACKEND_URL}/api/sessions/{selected_session_id}/history")
            if history_resp.status_code == 200:
                history_items = history_resp.json()
                if not history_items:
                    st.info("No activity recorded in this session yet.")
                else:
                    for item in history_items:
                        st.markdown(f"**[{item['specialist'].upper()}]** ({item['created_at'][:19]})")
                        st.write(item['text'])
                        st.markdown("---")
        except Exception as e:
            st.sidebar.error(f"Failed to fetch history: {e}")

        # Memory Operations Panel
        st.markdown("### 🔄 Memory Graph Consolidation")
        st.markdown("Bridge recent session interactions and Q&A history into the shared permanent memory graph.")

        if st.button("Trigger Self-Improvement ⚡"):
            with st.spinner("Consolidating graph and refining embeddings..."):
                try:
                    active_session_ids = [selected_session_id]
                    r = requests.post(f"{BACKEND_URL}/api/memory/improve", json=active_session_ids)
                    if r.status_code == 200:
                        st.success("Memory consolidated successfully! Embedding weights and summaries updated.")
                    else:
                        st.error(f"Self-improvement failed: {r.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

# Tab 2: Memory Inspector
with tab2:
    st.markdown("### 📂 Global Memory Auditor")
    st.write("Browse, search, and manage facts stored in MemoryOS.")

    # Search Bar
    search_q = st.text_input("🔍 Search Memory Database", placeholder="Type keywords to filter...")

    # Fetch Memories
    memories = []
    params = {}
    if search_q.strip():
        params["q"] = search_q.strip()
    
    try:
        m_resp = requests.get(f"{BACKEND_URL}/api/memory", params=params)
        if m_resp.status_code == 200:
            memories = m_resp.json()
    except Exception as e:
        st.error(f"Could not load memories: {e}")

    if not memories:
        st.info("No facts match the filter criteria.")
    else:
        st.write(f"Showing {len(memories)} entries:")
        for idx, mem in enumerate(memories):
            c1, c2 = st.columns([0.8, 0.2])
            with c1:
                st.markdown(f"**Entry {idx + 1}** - *Source: {mem['specialist'].upper()} Specialist* (Session: `{mem['session_id'][:8]}...`)")
                st.info(mem['text'])
                with st.expander("Show Metadata"):
                    st.json(mem['metadata'])
            with c2:
                # Add spacing to match button alignment
                st.write("")
                if st.button("Delete/Forget 🗑️", key=f"del_{mem['memory_id']}"):
                    try:
                        del_r = requests.delete(f"{BACKEND_URL}/api/memory/{mem['memory_id']}")
                        if del_r.status_code == 200:
                            st.success("Memory deleted!")
                            st.rerun()
                        else:
                            st.error(f"Failed to delete: {del_r.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
            st.markdown("---")
