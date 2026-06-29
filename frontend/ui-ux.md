# MemoryOS — ui-ux.md
### User flows, UX rationale, and design philosophy alignment
**Scope:** This week's build only (Developer + Learning specialists, Workspace, Memory Panel with Graph + Timeline tabs, `improve()` sequence). See `design.md` §9 for the deferred full-product IA.

---

## 1. The Core Feeling We're Designing For

The brief states it plainly: the user should think *"this AI actually remembers"*, not *"I'm chatting with another LLM."* Every decision in this document is a test against that one sentence. If a screen, a copy choice, or an animation doesn't make memory more visible, more alive, or more *earned* — it doesn't belong, no matter how nice it looks.

The brief also sets a hard, falsifiable bar: **persistent evolving memory must be understandable within 30 seconds of use.** That's not a vibe goal, it's a design constraint we can actually test against. Section 3 below is built around exactly those 30 seconds.

---

## 2. Primary User Flow (this week's scope)

```
Land on Workspace (Developer active by default)
        │
        ▼
See prior shallow answer already in thread
  (memory panel shows what WAS retrieved — 1 hop, low synthesis)
        │
        ▼
User asks the same/related question, OR clicks "Run improve()"
        │
        ▼
improve() sequence plays:
  progress bar → stats count in → "evolution complete"
        │
        ▼
Same question re-answered — now 3-hop, synthesizing
Learning's concept + Developer's implementation
        │
        ▼
Memory panel updates: new relationship card appears,
confidence rises, "why the AI knows this" explains the link
        │
        ▼
User switches to Learning specialist (pill, not dropdown)
        │
        ▼
Workspace instantly reframes (header, goal line, recall lens)
— but the SAME graph, SAME memory panel persists underneath
        │
        ▼
User asks Learning a question that only resolves correctly
because Developer's session fed the shared graph
        │
        ▼
Proof delivered: one memory, two reasoning modes, no isolation
```

This flow **is** the demo script from the PRD (§8), and that's deliberate — the UI isn't a generic shell the demo happens to run in, it's built around the specific proof we need to deliver to judges. UX and product strategy are the same document this week, not two separate concerns.

---

## 3. The First 30 Seconds (the brief's actual success metric)

Walking through exactly what a first-time viewer sees, in order, and why each beat exists:

| Time | What they see | Why it proves "memory," not "chat" |
|---|---|---|
| 0–3s | Topbar: `Graph · 14 nodes · 9 edges`, a pulsing green dot | A chat app has no reason to show you a node/edge count in its header. This single line says "there's a structure behind this" before a word of conversation is read. |
| 3–8s | Specialist pills with filled/empty rings, not a model-picker dropdown | Dropdowns say "pick a setting." Pills with rings say "pick a mind" — reframes specialists as identities, not configurations. |
| 8–15s | Right panel, permanently docked, showing live memory cards with confidence scores and source tags | The memory panel is never a "view source" afterthought button — it's always-on, same visual weight as the conversation. This is the single biggest IA decision in the whole spec, and it's a direct, literal execution of the brief's line: "Everything revolves around memory. Not chat." |
| 15–25s | The shallow → improve() → deep answer sequence | This is the moment abstract "self-improving memory" becomes a thing you watched happen, with a number (4 relationships, 2 merged, 1 removed) attached to it. Abstract claims about AI memory are cheap; a counter going up in front of you is not. |
| 25–30s | The "why the AI knows this" dashed card under the memory list | Closes the loop the brief explicitly asks for: *"the user should understand WHY the AI knows something."* Not just confidence scores — a sentence explaining the actual graph traversal. |

If a first-time viewer can narrate back "it has a graph, it has different specialist modes, and it just got smarter in front of me" after 30 seconds — the design has done its job. That's the literal acceptance test for this UI.

---

## 4. Why Each Major Decision Supports the Philosophy

### 4.1 Three-pane shell, memory panel always docked (never a drawer)
**Decision:** Memory panel is structurally permanent — same grid row as the workspace, not a toggleable overlay.
**Why:** A collapsible panel implies memory is optional context, summon-able when needed — exactly the "memory as retrieval feature" framing the brief rejects. A docked panel says memory is co-equal with conversation, structurally, not just rhetorically.

### 4.2 Pills/rings for specialist switching, not a dropdown
**Decision:** Specialists render as cards with a filled/empty ring indicator; switching animates the workspace header/context, not just the response style.
**Why:** Per brief: *"Switching specialists should instantly transform the workspace while preserving memory."* A dropdown is a settings metaphor — implies you're changing a parameter of one assistant. A pill switch with visible workspace reframing implies you're stepping into a different *mind* that happens to share your memory. The ring-fill animation specifically borrows from Arc Browser's tab-space switching, per the brief's named inspirations.

### 4.3 Mono font reserved exclusively for system/memory-state language
**Decision:** JetBrains Mono appears only in: topbar graph stats, recall-trace chips, timestamps, improve() stat numbers. Never in conversational text.
**Why:** This creates a learnable visual grammar with zero onboarding: *if it's monospace, it's the machine reporting on its own memory state; if it's sans-serif, it's reasoning addressed to you.* After seeing this pattern twice, a user doesn't need a legend — they've learned to read the interface's two registers. This directly serves "memory should be visible" without needing a tutorial.

### 4.4 `improve()` as a multi-stage animated sequence, not a toast/spinner
**Decision:** Progress bar → staggered stat reveal → completion state → answer changes below it, all visible in one continuous view.
**Why:** The brief calls this out as one of the most important interactions and explicitly wants the user to *"enjoy watching memory evolve."* A toast notification ("Memory updated") would be functionally equivalent but emotionally inert. The staggered reveal (relationships found, then merged, then deduped) mirrors how the brief itself sequences the example — we followed its own pacing, not a generic loading-state pattern.

### 4.5 Recall-trace chips on every AI answer (hop count + retrieval mode)
**Decision:** Every assistant message carries a small chip row: `3 hops · Learning → cost surface → Developer code` and `graph_completion`.
**Why:** Directly executes the brief's Memory Panel requirement: *"The user should understand WHY the AI knows something."* It also does real product work beyond aesthetics — for a hackathon judge specifically, this chip is the single clearest piece of evidence of multi-hop `GRAPH_COMPLETION` actually running, not faked. UX decision and judging-criteria evidence are the same artifact here.

### 6.6 Color discipline — purple reserved for relationships, amber reserved for "pre-improvement" state
**Decision:** Purple never appears on a button or primary action. Amber never appears as a generic warning — only as the left-border marker on a shallow/before-improve answer.
**Why:** If every accent color could mean anything, none of them would mean something specific. Scarcity makes color load-bearing: see purple → think "this is about a relationship between concepts." See amber on a message → think "this answer predates improvement." That single left-border amber stripe is doing real explanatory work without a single word of label text.

### 4.7 Timeline as "story of memory," not chat history
**Decision:** Timeline tab shows discrete memory *events* (remember, recall-shallow, improve, recall-deep) as a vertical story with faded/unfaded states for past-vs-current relevance — not a scrollback of every message.
**Why:** Brief explicitly specs this structure (Learning Session → Memory Created → Developer Used Memory → improve() → New Relationships → Future Suggestions) and explicitly says *"replace chat history."* Faded older items aren't just style — they encode that older session memory has already been folded into the permanent graph and is no longer the "live" story, which is a true fact about the system's state, not decoration.

### 4.8 Small, always-present graph preview (not a full-screen graph explorer, this week)
**Decision:** A ~220px graph view with gently floating nodes, always visible in the Memory Panel; "Expand ↗" affordance present but not wired yet.
**Why:** Brief: *"The graph is NOT a gimmick... Small. Elegant. Interactive. Expandable. It should look alive."* The floating-node micro-animation is the one piece of ambient motion in an otherwise calm, static interface — motion is spent here specifically because this is the one element the brief insists must feel alive, per the frontend-design skill's instruction to spend boldness in one place rather than scattering it.

### 4.9 What we deliberately did NOT build this week, and why that's also a UX decision
**Decision:** Projects and Settings appear in nav, visibly, with a "SOON" tag — disabled, not hidden.
**Why:** Hiding them entirely would make the IA feel smaller than the product's real ambition; building them this week would dilute build time away from the improve() proof that actually wins judging criteria. Showing-but-disabling is itself a UX statement: "this is a real operating system with a real roadmap, and we know exactly what's not done yet" — which is more credible to a sophisticated judge than either pretending the bigger vision doesn't exist or half-building it badly.

---

## 5. Flow: Specialist Switch (detail)

```
[Developer pill active] → user clicks [Learning pill]
        │
        ├─ Ring fill animates: Developer's ring empties (200ms),
        │  Learning's ring fills (200ms, staggered)
        │
        ├─ Workspace crumb updates: "SPECIALIST / DEVELOPER" → "SPECIALIST / LEARNING"
        │
        ├─ H1 + goal line swap (instant, no skeleton/loading state —
        │  this is a context switch, not a data fetch, and should feel as fast as one)
        │
        └─ Memory Panel does NOT reset — same graph, same timeline,
           proving shared memory by simply... not changing
```

The deliberate absence of a loading state on switch is itself a claim: specialists are reasoning *lenses* over one already-loaded memory, not separate apps that each need their own fetch. If switching ever needs a spinner, that would silently contradict the "one shared memory" premise the whole product is built on.

---

## 6. Empty / Error States (per frontend-design writing guidance)

Per the skill's guidance to treat emptiness as direction, not mood:

- **Empty graph (no memory yet):** *"Nothing remembered yet. Ask Developer or Learning something, and memory starts here."* — not "No data available."
- **`improve()` with nothing new to find:** *"No new relationships this pass — memory is already well-connected."* Framed as a status, not a failure.
- **Recall finds nothing relevant:** *"Nothing in memory connects to this yet."* — names the actual system state (a graph gap) rather than a generic "no results."

---

## 7. Open Items for Post-Hackathon Rebuild

- Full-screen graph explorer (pan/zoom) — this week's preview is intentionally small per brief
- Settings (LLM provider, ontology config, dataset management)
- Projects (multi-project memory scoping — separate graphs or filtered views per project)
- Research / Planner as fully built workspaces with their own recall lenses
- Mobile-first pass (see `design.md` §6 for the collapse strategy already specced)

These are not gaps in this week's thinking — they're the explicitly deferred remainder of the original brief, tracked here so the rebuild starts from "what's left" rather than from zero.
