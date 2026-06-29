# API Reference

MemoryOS exposes a REST API via FastAPI.

## Endpoints

### 1. Sessions
* **POST `/api/sessions`**
  - Description: Create a new user session.
  - Response: `{"session_id": "uuid", "created_at": "timestamp"}`

* **GET `/api/sessions`**
  - Description: List all active and past sessions.
  - Response: `[{"session_id": "uuid", "created_at": "timestamp"}]`

* **DELETE `/api/sessions/{session_id}`**
  - Description: Delete a session and its temporary metadata.
  - Response: `{"status": "deleted"}`

### 2. Specialists
* **POST `/api/specialists/learner`**
  - Description: Run the Learner Specialist to ingest raw text and trigger `remember`.
  - Request Body: `{"session_id": "uuid", "text": "Raw information to learn"}`
  - Response: `{"status": "remembered", "facts_extracted": []}`

* **POST `/api/specialists/developer`**
  - Description: Run the Developer Specialist to retrieve context and answer questions/generate code.
  - Request Body: `{"session_id": "uuid", "query": "Coding question or prompt"}`
  - Response: `{"answer": "Generated response based on recalled memories"}`

### 3. Memory Operations
* **POST `/api/memory/improve`**
  - Description: Consolidate and refine the persistent memory graph.
  - Response: `{"status": "improved"}`
