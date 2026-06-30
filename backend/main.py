"""FastAPI Main entry point for MemoryOS backend.

This module sets up routes for session management, specialist workflows,
and memory improvement, and handles database migrations on startup.
"""

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


from memory.cognee_adapter import setup_cognee
from memory.improve import improve_memory
from orchestrator.session_manager import SessionManager
from orchestrator.workflow_engine import WorkflowEngine
from config.settings import settings, verify_settings_on_startup
from backend.core.groq_client import get_groq_client, check_groq_connectivity
from orchestrator.graph_viewer import generate_svg_graph


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown operations."""
    # 1. Verify settings (exits on fatal error)
    verify_settings_on_startup()

    # 2. Initialize Groq client
    try:
        get_groq_client()
        logger.info("Groq client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Groq client: {e}")

    # 3. Initialize Cognee
    logger.info("Initializing Cognee on backend startup...")
    try:
        await setup_cognee()
        logger.info("Cognee startup setup completed.")
    except Exception as e:
        logger.error(f"Error during Cognee startup setup: {e}")
    yield
    logger.info("Backend shutting down...")

app = FastAPI(
    title="MemoryOS API",
    description="One Memory. Infinite Thinking Modes.",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware for stream and client integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_manager = SessionManager()
workflow_engine = WorkflowEngine(session_manager)

# Request schemas
class IngestRequest(BaseModel):
    session_id: str
    text: str

class QueryRequest(BaseModel):
    session_id: str
    query: str

class RouteRequest(BaseModel):
    session_id: str
    text: str

class SessionCreateRequest(BaseModel):
    metadata: Optional[Dict[str, Any]] = None

@app.get("/")
def read_root() -> Any:
    """Serve the index.html frontend."""
    from fastapi.responses import HTMLResponse
    import os
    html_path = os.path.join("frontend", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>MemoryOS Frontend Not Found</h1>", status_code=404)

@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    """Comprehensive health check: backend, Groq, models, database, Cognee."""
    import os

    # Groq connectivity
    groq_status = check_groq_connectivity()

    # Database status
    db_exists = os.path.exists("metadata.db")

    # Cognee status
    try:
        import cognee
        cognee_version = getattr(cognee, "__version__", "unknown")
        cognee_status = "available"
    except Exception:
        cognee_version = None
        cognee_status = "unavailable"

    return {
        "backend": "running",
        "groq": groq_status,
        "models": {
            "planner": settings.planner_model,
            "developer": settings.developer_model,
            "learner": settings.learner_model,
            "classifier": settings.classifier_model,
        },
        "database": {
            "provider": settings.db_provider,
            "metadata_db_exists": db_exists,
        },
        "cognee": {
            "status": cognee_status,
            "version": cognee_version,
        },
    }

# Session endpoints
@app.post("/api/sessions")
def create_session(request: SessionCreateRequest) -> Dict[str, Any]:
    """Create a new session."""
    try:
        return session_manager.create_session(metadata=request.metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions")
def list_sessions() -> List[Dict[str, Any]]:
    """List all user sessions."""
    try:
        return session_manager.list_sessions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sessions/{session_id}/complete")
async def complete_session(session_id: str) -> Dict[str, Any]:
    """Mark a session completed and trigger memory improvements."""
    try:
        return await workflow_engine.complete_session(session_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str) -> Dict[str, str]:
    """Delete a session."""
    success = session_manager.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}

# Specialist workflow endpoints
@app.post("/api/specialists/route")
async def route_specialist(request: RouteRequest) -> Dict[str, Any]:
    """Classify and route the query automatically to the correct specialist."""
    try:
        return await workflow_engine.route_request(
            session_id=request.session_id,
            text=request.text
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/specialists/learner")
async def run_learner(request: IngestRequest) -> Dict[str, Any]:
    """Execute Learner Specialist workflow to ingest info."""
    try:
        return await workflow_engine.execute_learner_flow(
            session_id=request.session_id,
            text=request.text
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/specialists/developer")
async def run_developer(request: QueryRequest) -> Dict[str, Any]:
    """Execute Developer Specialist workflow to retrieve memory and generate code."""
    try:
        return await workflow_engine.execute_developer_flow(
            session_id=request.session_id,
            query=request.query
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/specialists/planner")
async def run_planner(request: QueryRequest) -> Dict[str, Any]:
    """Execute Planner Specialist workflow to retrieve memory and generate roadmaps."""
    try:
        return await workflow_engine.execute_planner_flow(
            session_id=request.session_id,
            query=request.query
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/specialists/researcher")
async def run_researcher(request: QueryRequest) -> Dict[str, Any]:
    """Execute Researcher Specialist workflow to recall concepts and synthesize summaries."""
    try:
        return await workflow_engine.execute_researcher_flow(
            session_id=request.session_id,
            query=request.query
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/graph/svg")
def get_graph_svg(session_id: Optional[str] = None) -> HTMLResponse:
    """Generate and return the SVG Knowledge Graph for a session."""
    try:
        memories = session_manager.list_memories(session_id=session_id)
        svg_content = generate_svg_graph(memories, active_session_id=session_id or "")
        return HTMLResponse(content=svg_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Memory operations endpoints

@app.get("/api/memory")
def get_memories(session_id: Optional[str] = None, q: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all logged memories, with optional session filtering and text query search."""
    try:
        if q:
            return session_manager.search_memories(query=q, session_id=session_id)
        return session_manager.list_memories(session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}/history")
def get_history(session_id: str) -> List[Dict[str, Any]]:
    """Get the full history/log of actions within a specific session."""
    try:
        return session_manager.get_session_history(session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/memory/{memory_id}")
def delete_memory_log(memory_id: str) -> Dict[str, str]:
    """Delete a specific logged memory entry."""
    success = session_manager.delete_memory_log(memory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Memory entry not found")
    return {"status": "deleted"}

@app.post("/api/memory/improve")
async def run_improve(session_ids: Optional[List[str]] = Body(None)) -> Dict[str, Any]:
    """Trigger memory consolidation for the specified sessions."""
    try:
        result = await improve_memory(session_ids=session_ids)
        return {"status": "improved", "details": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PromoteRequest(BaseModel):
    session_id: str


@app.post("/api/graph/promote")
async def promote_graph(request: PromoteRequest) -> Dict[str, Any]:
    """Analyze temporary session graph learner facts, extract keywords/concepts, and promote to the permanent graph."""
    session_id = request.session_id
    memories = session_manager.list_memories(session_id=session_id)
    learner_facts = [m["text"] for m in memories if m["specialist"] == "learner"]

    if not learner_facts:
        return {"status": "skipped", "message": "No facts available in this session to promote."}

    try:
        import sqlite3
        import cognee

        stop_words = {
            "is", "a", "an", "the", "and", "or", "in", "on", "at", "for", "to", "of", "with", "about", 
            "are", "you", "to", "be", "was", "were", "has", "have", "had", "been", "will", "would", 
            "shall", "should", "can", "could", "may", "might", "must", "us", "we", "i", "my", "me", 
            "he", "she", "they", "them", "it", "its", "their", "his", "her", "as", "by", "from", "into",
            "out", "over", "under", "again", "then", "once", "here", "there", "when", "where", "why", 
            "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", 
            "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", 
            "just", "don", "should", "now", "using", "used", "make", "made", "does", "do", "did"
        }

        promoted_count = 0
        added_node_ids = {}

        for fact in learner_facts:
            # Clean words
            words = []
            for w in fact.split():
                w_clean = w.strip(".,?!();:\"'").strip()
                if w_clean:
                    words.append(w_clean)

            important_words = []
            for w in words:
                if w.lower() not in stop_words and len(w) > 2:
                    important_words.append(w)

            if not important_words:
                continue

            # First word (or first capitalized word) is main concept
            main_word = important_words[0]
            for w in important_words[1:]:
                if w[0].isupper():
                    main_word = w
                    break

            main_color = "#A88BEB" # Purple for main concepts
            main_desc = f"Main concept from: {fact}"
            main_id = session_manager.add_permanent_node(main_word, "main", main_color, main_desc)
            added_node_ids[main_word] = main_id
            promoted_count += 1

            for child_word in important_words:
                if child_word == main_word:
                    continue
                child_color = "#FF8A8A" # Red/pink for child terms
                child_desc = f"Term related to {main_word} in session memory"
                child_id = session_manager.add_permanent_node(child_word, "child", child_color, child_desc)
                added_node_ids[child_word] = child_id
                
                # Add link
                session_manager.add_permanent_edge(child_id, main_id, "parent-child")

        # Optionally run Cognee improve to keep everything aligned
        try:
            await cognee.improve()
        except Exception as ie:
            logger.error(f"Cognee improve during promotion skipped or failed: {ie}")

        return {"status": "success", "message": f"Successfully promoted {promoted_count} session concepts to the Permanent Graph."}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Promotion failed: {str(ex)}")


@app.get("/api/graph/permanent/svg")
def get_permanent_graph_svg() -> HTMLResponse:
    """Generate and return the Permanent Knowledge Graph SVG representation."""
    try:
        nodes = session_manager.get_permanent_nodes()
        edges = session_manager.get_permanent_edges()
        from orchestrator.graph_viewer import generate_permanent_svg_graph
        svg_content = generate_permanent_svg_graph(nodes, edges)
        return HTMLResponse(content=svg_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


