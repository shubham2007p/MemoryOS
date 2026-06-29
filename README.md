<p align="center">
  <br>
  <img alt="MemoryOS" src="https://img.shields.io/badge/%F0%9F%A7%A0-MemoryOS-4D8DFF?style=for-the-badge&labelColor=0A0B0E&logoColor=white" height="50">
</p>

<h1 align="center">MemoryOS</h1>

<p align="center">
  <strong>One Memory. Infinite Thinking Modes.</strong>
</p>

<p align="center">
  <em>AI that remembers, evolves, and shares knowledge across specialist reasoning modes.</em>
</p>

<br>

<p align="center">
  <a href="https://github.com/shubham2007p/MemoryOS/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-0969da?style=for-the-badge&labelColor=1a1a2e" alt="License"></a>&nbsp;
  <a href="https://github.com/shubham2007p/MemoryOS/stargazers"><img src="https://img.shields.io/badge/Stars-⭐_Star_This_Repo-e3b341?style=for-the-badge&labelColor=1a1a2e" alt="Stars"></a>&nbsp;
  <img src="https://img.shields.io/badge/Built_With-Cognee-9B7CFF?style=for-the-badge&labelColor=1a1a2e" alt="Cognee">&nbsp;
  <img src="https://img.shields.io/badge/Python-3.13-34D399?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e" alt="Python 3.13">&nbsp;
  <img src="https://img.shields.io/badge/Status-MVP-F2B544?style=for-the-badge&labelColor=1a1a2e" alt="Status">
</p>

<p align="center">
  <a href="#-the-problem">The Problem</a>&ensp;·&ensp;
  <a href="#-how-it-works">How It Works</a>&ensp;·&ensp;
  <a href="#-features">Features</a>&ensp;·&ensp;
  <a href="#-quick-start">Quick Start</a>&ensp;·&ensp;
  <a href="#-architecture">Architecture</a>&ensp;·&ensp;
  <a href="#-roadmap">Roadmap</a>
</p>

<br>

---

<br>

## 🧩 The Problem

You're working across multiple projects. You open an AI assistant to ask a question.

The AI has **zero memory**:

| What the AI forgets | Why it matters |
| :--- | :--- |
| What you taught it yesterday | Every conversation starts from scratch |
| Context from your other projects | Knowledge stays siloed and fragmented |
| How concepts connect across domains | It can't synthesize cross-domain insights |
| What it already figured out for you | It wastes time re-deriving the same conclusions |

**Result?** You spend more time re-explaining context than actually thinking.

**MemoryOS eliminates this entirely.**

<br>

## ⚡ How It Works

```
┌──────────────┐     ┌───────────────────┐     ┌──────────────────┐
│   You        │────▶│    MemoryOS       │────▶│  AI Specialists  │
│              │     │                   │     │                  │
│ • Questions  │     │ • remember()      │     │ ✓ Developer      │
│ • Knowledge  │     │ • recall()        │     │ ✓ Learning       │
│ • Context    │     │ • improve()       │     │ ✓ Research  soon │
└──────────────┘     └───────────────────┘     └──────────────────┘
                              │
                     ┌────────┴────────┐
                     │  Cognee Graph   │
                     │  + Vector DB    │
                     │  Persistent     │
                     │  Shared Memory  │
                     └─────────────────┘
```

Memory belongs to **you**, not to any single specialist. Every specialist reasons over the **same evolving graph** — so learning improves development, and development feeds back into learning.

<br>

## ✨ Features

### Memory Lifecycle

<table>
  <tr>
    <td width="33%" align="center">
      <h4>📥 remember()</h4>
      <p>Ingest knowledge into the<br>persistent graph memory.<br>Facts, code, concepts — all indexed.</p>
    </td>
    <td width="33%" align="center">
      <h4>🔍 recall()</h4>
      <p>Query memory with multi-hop<br>graph traversal. Context is<br>retrieved, not hallucinated.</p>
    </td>
    <td width="33%" align="center">
      <h4>🧬 improve()</h4>
      <p>Self-evolving memory consolidation.<br>Finds relationships, merges concepts,<br>removes duplicates automatically.</p>
    </td>
  </tr>
</table>

### Core Capabilities

| Feature | Description |
| :--- | :--- |
| **Persistent Graph Memory** | Knowledge survives across sessions, powered by Cognee's graph + vector store |
| **Specialist System** | Developer and Learning modes reason differently over the same shared memory |
| **Session Management** | Full CRUD lifecycle — create, switch, delete sessions with metadata tracking |
| **Workflow Engine** | Automatic input classification routes statements to Learning, questions to Developer |
| **Memory Evolution** | `improve()` consolidates, deduplicates, and strengthens graph relationships |
| **Live Knowledge Graph** | Real-time SVG visualization of your memory network with node/edge stats |
| **Context Tracing** | Every AI answer shows retrieval path — hop count, source specialist, graph mode |

<br>

## 📋 Demo Flow

<details>
<summary><strong>🧬 The improve() Proof</strong> (click to expand)</summary>

```
1. Ask Developer: "Why does gradient descent need feature scaling?"
   → Shallow answer: "It helps convergence" (1 hop, code chunk only)

2. Click "Run improve()"
   → Memory evolution: 4 relationships found · 2 concepts merged · 1 duplicate removed

3. Ask the same question again
   → Deep answer: Synthesizes Learning's cost-surface notes + Developer's
     standardization code across 3 hops, explaining WHY one shared learning
     rate requires normalized features

4. Switch to Learning specialist
   → Same graph, same memory — different reasoning lens
   → Learning can now answer implementation questions because Developer
     fed the shared graph
```

**This is the core proof:** one memory, two reasoning modes, no isolation.

</details>

<details>
<summary><strong>🖥️ UI Architecture</strong> (click to expand)</summary>

```
┌──────────┬─────────────────────────────┬────────────┐
│  brand   │  topbar: graph stats · ●    │            │
├──────────┼─────────────────────────────┼────────────┤
│ Workspace│  crumb / title / goal       │ Memory|Time│
│ Timeline │                             │            │
│ Graph    │  [shallow answer]           │ [graph viz]│
│ Projects*│  [improve() banner]         │            │
│ Settings*│  [deep answer]              │ [retrieved │
│          │                             │  cards]    │
│ ———————  │                             │            │
│ Developer│                             │ [why AI    │
│ Learning │  [composer + Run improve()] │  knows]    │
│ Research*│                             │            │
│ Planner* │                             │            │
└──────────┴─────────────────────────────┴────────────┘
   * = visible, disabled — future roadmap
```

</details>

<br>

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- A Groq API key (or OpenAI / Gemini key)

### Installation

```bash
git clone https://github.com/shubham2007p/MemoryOS.git
cd MemoryOS
```

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

See [`memoryos_user_input.md`](memoryos_user_input.md) for the full list of configurable environment variables, metadata fields, and model mappings.

### Run

```bash
# Start the server (serves both API and frontend)
uvicorn backend.main:app --port 8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

<br>

## 🏛️ Architecture

```
Frontend (HTML/JS)  ──▶  FastAPI Backend  ──▶  Orchestrator
                                │                   │
                           Session Manager      Workflow Engine
                                │                   │
                           SQLite Metadata    ┌─────┴──────┐
                                              │            │
                                           Learner    Developer
                                              │            │
                                              ▼            ▼
                                        ┌──────────────────────┐
                                        │   Cognee Memory      │
                                        │  (Graph + Vector DB) │
                                        │                      │
                                        │  remember() / recall()│
                                        │  improve() / forget() │
                                        └──────────────────────┘
```

### Repository Structure

```
MemoryOS/
├── backend/          # FastAPI server, API routes, serves frontend
├── frontend/         # HTML/JS client with design specs
├── memory/           # remember, recall, improve, cognee_adapter
├── orchestrator/     # session_manager, workflow_engine, graph_viewer
├── specialists/      # learner, developer (+ future: research, planner)
├── config/           # settings, prompts, templates
├── tests/            # unit + integration tests (26 passing)
├── docs/             # architecture, PRD, manifesto, decisions
└── status/           # current state tracking
```

<br>

## 🗺️ Roadmap

| Milestone | Status | Deliverables |
| :--- | :---: | :--- |
| **M1 — Infrastructure** | ✅ Done | Cognee integration, session management, workflow engine, test suite |
| **M2 — Core Intelligence** | ✅ Done | Specialist system, classification routing, metadata mapping, prompt templates |
| **M3 — Functional MVP** | ✅ Done | Memory CRUD API, retrieval pipeline, memory search, Streamlit dashboard |
| **M4 — Product Experience** | ✅ Done | Knowledge graph viz, improve() evolution feedback, context tracing, timeline |
| **M5 — Production UI** | ✅ Done | Custom HTML frontend, design-system integration, FastAPI-served SPA |
| **M6 — Scale** | 📋 Planned | Research + Planner specialists, multi-project scoping, full graph explorer |

<br>

## 🏗️ Tech Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">&nbsp;
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">&nbsp;
  <img src="https://img.shields.io/badge/Cognee-9B7CFF?style=for-the-badge&labelColor=1a1a2e" alt="Cognee">&nbsp;
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">&nbsp;
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">&nbsp;
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
</p>

<br>

## 📖 Documentation

New contributors should begin with:

```
START_HERE.md
```

Then continue through the numbered documents in the [`docs/`](docs/) directory:

| File | Purpose |
| :--- | :--- |
| `00_PROJECT.md` | Project overview |
| `01_MANIFESTO.md` | Design philosophy |
| `02_PRD.md` | Product requirements |
| `03_ARCHITECTURE.md` | System architecture |
| `05_MEMORY.md` | Memory model design |
| `10_DECISIONS.md` | Architectural decision log |
| `11_RULES.md` | Development rules |
| `13_TASKS.md` | Task tracking |

<br>

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

<br>

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

<br>

---

<p align="center">
  <sub>Built for the <strong>Cognee Hackathon</strong> by <a href="https://github.com/shubham2007p">@shubham2007p</a></sub>
</p>
