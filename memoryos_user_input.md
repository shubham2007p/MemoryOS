# MemoryOS Project Dependencies and User Inputs

This document lists all system dependencies, environment variables, metadata keys, and configuration requirements needed to run and configure MemoryOS.

---

## 1. Environment Configuration (`.env`)

These environment variables are loaded by `config/settings.py` to bootstrap Cognee and LLM providers.

### API Keys
- `GROQ_API_KEY`: Required. Primary API key for specialist reasoning (`groq/llama3-8b-8192` and `groq/llama3-70b-8192`).
- `GEMINI_API_KEY`: Optional. Fallback/alternative reasoning provider.
- `OPENAI_API_KEY`: Optional. Can be configured for Cognee standard embeddings if needed.
- `COGNEE_API_KEY`: Optional. For cloud/hosted Cognee integrations.

### Database Settings
- `DB_PROVIDER`: Default: `sqlite`. Relational database provider for Cognee metadata.
- `VECTOR_DB_PROVIDER`: Default: `lancedb`. Vector storage provider.
- `GRAPH_DB_PROVIDER`: Default: `kuzu`. Graph database provider.

### URL & Networking
- `BACKEND_URL`: Default: `http://localhost:8000`. Frontend connection string.

---

## 2. Ingestion Metadata Fields

When calling `remember_data()` or logging facts in `SessionManager.add_memory_log()`, the following metadata fields are tracked:

| Key | Type | Description |
|---|---|---|
| `session_id` | String (UUID) | Identifies the session grouping. |
| `timestamp` | String (ISO 8601) | Recording date/time. |
| `specialist` | String | Originating specialist mode (`learner` or `developer`). |
| `source` | String | Input channel (`user_input`, `repo_file`, etc.). |
| `importance` | String | Prioritization level (`high`, `medium`, `low`). |
| `confidence` | Float | Confidence level (`0.0` to `1.0`). |

---

## 3. Specialist Model Mappings

These settings define which models are loaded for each cognitive specialist:
- **Learner Specialist**: `groq/llama3-8b-8192`
- **Developer Specialist**: `groq/llama3-70b-8192`
- **Classifier Router**: `groq/llama3-8b-8192`
