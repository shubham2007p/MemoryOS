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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown operations."""
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

class SessionCreateRequest(BaseModel):
    metadata: Optional[Dict[str, Any]] = None

@app.get("/")
def read_root() -> Dict[str, str]:
    """Base endpoint to check backend health."""
    return {"name": "MemoryOS API", "version": "0.1.0"}

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

@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str) -> Dict[str, str]:
    """Delete a session."""
    success = session_manager.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}

# Specialist workflow endpoints
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

# Memory operations endpoints
@app.post("/api/memory/improve")
async def run_improve(session_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """Trigger memory consolidation for the specified sessions."""
    try:
        result = await improve_memory(session_ids=session_ids)
        return {"status": "improved", "details": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
