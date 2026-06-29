# 🧠 MemoryOS

> **One Memory. Infinite Thinking Modes.**

MemoryOS is a persistent cognitive operating system built on top of **Cognee**.

Instead of treating memory as chat history, MemoryOS treats memory as a first-class capability that continuously evolves and is shared across specialized AI reasoning modes.

---

# Why MemoryOS?

Today's AI forgets.

Every new conversation starts from scratch.

Knowledge becomes fragmented across chats, notes, documents and projects.

MemoryOS explores a different future.

A future where AI specialists share one evolving memory and continuously improve over time.

---

# Core Idea

Memory belongs to the user.

Specialists do not own memory.

They reason differently over the same persistent knowledge.

```
User
   │
   ▼
MemoryOS
   │
   ▼
Shared Cognee Memory
   │
 ┌─┼───────────────┐
 │ │               │
 ▼ ▼               ▼
Learning      Developer
Research      Planner
```

Learning should improve development.

Research should improve planning.

Everything compounds.

---

# Built With

* Python
* FastAPI
* Streamlit
* Cognee
* SQLite
* Graph + Vector Memory

---

# Current MVP

* Persistent Memory
* Learning Specialist
* Developer Specialist
* Session Management
* Workflow Engine
* Memory Lifecycle
* `remember()`
* `recall()`
* `improve()`

---

# Memory Lifecycle

```
Session

↓

remember()

↓

Persistent Graph Memory

↓

recall()

↓

Specialist Reasoning

↓

improve()

↓

Stronger Memory
```

---

# Repository Structure

```
backend/
frontend/
memory/
orchestrator/
specialists/
docs/
engineering/
knowledge/
tests/
```

---

# Development Philosophy

MemoryOS is built documentation-first.

Every architectural decision is documented before implementation.

AI coding agents use the documentation as the project's source of truth.

---

# Getting Started

Clone the repository.

```bash
git clone https://github.com/<username>/MemoryOS.git
```

Create a virtual environment.

```bash
python -m venv .venv
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the backend.

```bash
uvicorn backend.main:app --reload
```

Run the frontend.

```bash
streamlit run frontend/app.py
```

---

# Documentation

New contributors should begin with:

```
START_HERE.md
```

Then continue through the numbered documents in the `docs/` directory.

---

# Vision

MemoryOS is more than a chatbot.

It is an experiment in persistent cognition.

The long-term goal is to explore what software becomes possible once AI no longer forgets.

---

# Status

🚧 Active Development

Built for the Cognee Hackathon.
