"""FastAPI Main entry point for MemoryOS backend.

This module sets up routes for session management, specialist workflows,
and memory improvement, and handles database migrations on startup.
"""

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from memory.cognee_adapter import setup_cognee
from memory.improve import improve_memory
from orchestrator.session_manager import SessionManager
from orchestrator.workflow_engine import WorkflowEngine
from config.settings import settings, verify_settings_on_startup
from backend.core.groq_client import get_groq_client, check_groq_connectivity

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
async def run_improve(session_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """Trigger memory consolidation for the specified sessions."""
    try:
        result = await improve_memory(session_ids=session_ids)
        return {"status": "improved", "details": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


