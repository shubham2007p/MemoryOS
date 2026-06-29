# START_HERE.md

# Welcome to MemoryOS

If you're reading this, you're either:

* A developer joining the project
* An AI coding agent
* A contributor
* Or future us returning after weeks or months

This document is your entry point.

Do **not** start coding yet.

Read this file completely.

---

# What is MemoryOS?

MemoryOS is a persistent cognitive operating system built on top of Cognee.

Cognee provides:

* Persistent Memory
* Knowledge Graph
* Graph + Vector Retrieval
* Memory Evolution (`remember()`, `recall()`, `improve()`)

MemoryOS provides:

* Specialist orchestration
* Sessions
* Workflows
* User experience
* Reasoning
* Collaboration

MemoryOS is **not** another chatbot.

MemoryOS explores what software becomes possible once AI no longer forgets.

---

# Core Philosophy

One Memory.

Infinite Thinking Modes.

Memory belongs to the user.

Specialists never own memory.

They only reason differently over the same memory.

---

# Before Writing Code

Read these files in order.

1.

`docs/00_PROJECT.md`

↓

2.

`docs/01_MANIFESTO.md`

↓

3.

`docs/02_PRD.md`

↓

4.

`docs/03_ARCHITECTURE.md`

↓

5.

`docs/05_MEMORY.md`

↓

6.

`docs/10_DECISIONS.md`

↓

7.

`docs/11_RULES.md`

↓

8.

`status/CURRENT_STATE.md`

Do not skip this order.

---

# Source of Truth

If documentation and code disagree,

documentation wins.

Architecture must never be inferred from implementation.

---

# Repository Structure

High level:

```text
Frontend

↓

FastAPI Backend

↓

Orchestrator

↓

Cognee Memory

↓

Persistent Knowledge Graph
```

Never bypass this architecture.

---

# Development Workflow

Every feature follows the same lifecycle.

Task

↓

Read documentation

↓

Implement

↓

Test

↓

Review

↓

Update documentation

↓

Commit

↓

Push

↓

Close Task

Never skip steps.

---

# Git Workflow

Never commit unfinished work.

Commit only after one complete task.

Commit message examples:

feat(memory): add remember trigger

fix(session): resolve duplicate sessions

docs(prd): update workflow

refactor(orchestrator): simplify routing

---

# Branch Strategy

Never work directly on main.

main

↓

dev

↓

feature/<feature-name>

↓

merge

---

# AI Development Rules

Every AI agent must:

✓ Read documentation first

✓ Follow architecture

✓ Implement one task only

✓ Never invent architecture

✓ Never duplicate permanent memory

✓ Never bypass Cognee

✓ Never modify unrelated modules

✓ Update documentation if needed

---

# Current Sprint

Always read:

`status/CURRENT_STATE.md`

This file tells you:

* Current Sprint
* Current Task
* Blockers
* Next Milestone

Never assume.

---

# Current Task

Do not decide your own task.

Open:

`docs/13_TASKS.md`

Find the first unfinished task.

Implement only that task.

---

# Definition of Done

A task is complete only when:

✓ Acceptance Criteria satisfied

✓ Tests pass

✓ Documentation updated

✓ Code reviewed

✓ Commit created

✓ Ready for merge

---

# Project Principles

1.

Memory is shared.

Not duplicated.

---

2.

Sessions are temporary.

Memory is permanent.

---

3.

Specialists think differently.

They do not remember differently.

---

4.

Memory evolves intentionally.

Not continuously.

---

5.

Every feature must strengthen the shared memory.

Never bypass it.

---

# Things You Must Never Change

Unless explicitly approved:

* Core Architecture
* Cognee ownership of permanent memory
* Session lifecycle
* Specialist responsibilities
* Repository structure
* Engineering principles

---

# If You're an AI Coding Agent

Your workflow is:

Read documentation

↓

Read current task

↓

Implement only current task

↓

Run tests

↓

Self-review

↓

Update documentation

↓

Return modified files

Do not continue to another task.

---

# If You Get Lost

Read these three files again:

1.

Architecture

2.

Decisions

3.

Current State

The answer should already exist.

Never guess.

---

# Long-Term Vision

The hackathon MVP is only the first milestone.

The long-term vision is a persistent cognitive operating system where multiple reasoning specialists continuously build upon one evolving memory.

Everything in this repository should move that vision forward.

---

# Final Rule

The goal is **not to write the most code.**

The goal is to build the clearest demonstration that persistent, evolving memory fundamentally changes how AI systems collaborate and improve over time.

If a feature does not strengthen that story,

it does not belong in the MVP.
