# MemoryOS — design.md
### Design system, tokens, and component code
**Scope note:** This document specs only the screens we are actually building this hackathon week — **Workspace (chat), Specialist Switcher, Memory Panel, Graph view, Timeline, and the `improve()` sequence.** Projects and Settings exist as visible-but-disabled nav items only (future placeholders), not designed screens. Full IA (Memory/Workspace/Graph/Projects/Settings as equal top-level destinations) is the eventual MemoryOS vision and is deferred — see Section 9.

---

## 1. Design Plan (brainstorm pass, per frontend-design process)

**Subject:** A cognitive operating system where memory — not chat — is the primary object. The brief explicitly forbids the ChatGPT/Claude/Perplexity sidebar-and-bubbles template, and names Linear, Raycast, Cursor, Arc, and Apple HIG as reference points. Audience: technical builders who will judge this on whether memory *feels alive*, not on conversational warmth.

**Color (4–6 named hex values):**
- `--bg-0 #0A0B0E` — near-black charcoal, the void the graph floats in
- `--accent #4D8DFF` — electric blue, reserved for "this is memory, this is active, this is alive"
- `--purple #9B7CFF` — secondary accent, used only for cross-domain/relationship signals (edges, hop indicators) — never for primary actions, so it stays meaningful
- `--emerald #34D399` — success / high-confidence / live status only
- `--amber #F2B544` — "shallow" or pre-improve state marker — a warning that memory hasn't connected yet, not an error

**Type (2+ roles):**
- Display: Inter at 600 weight, tight letter-spacing (-0.01em) — used sparingly, only for screen titles and the `improve()` headline. Not a typographic flex; the brief asks for calm, not loud.
- Body: Inter at 400/500 — same family as display, different weight, deliberately: this product's personality is precision and restraint, not a display-face moment. A second decorative face would fight the "calm operating system" brief.
- Mono: JetBrains Mono — used **only** for system-state language (timestamps, recall-trace chips, node/edge counts, the topbar status line). This is the one structural device that actually encodes something true: mono = "this is the machine talking about its own memory," sans = "this is reasoning, addressed to you."

**Layout concept:**
Three-pane shell — nav (specialists + future nav) / workspace (chat-as-reasoning, not chat-as-messaging) / memory panel (always visible, never a modal). The memory panel is permanently docked, not a drawer you open — because the brief's core instruction is "the graph is the heart of the product, not chat," and a collapsible panel would let users hide the heart. Three-pane over two-pane was the deliberate call.

```
┌──────────┬─────────────────────────────┬────────────┐
│  brand   │  topbar: graph stat · ⌘k   │            │
├──────────┼─────────────────────────────┼────────────┤
│ Workspace│  crumb / title / goal       │ Memory|Time│
│ Timeline │                             │            │
│ Graph    │  [shallow answer]           │ [graph viz]│
│ Projects*│  [improve() banner]         │            │
│ Settings*│  [deep answer]              │ [retrieved │
│          │                             │  cards]    │
│ —————    │                             │            │
│ Developer│                             │ [why AI    │
│ Learning │  [composer + Run improve()] │  knows]    │
│ Research*│                             │            │
│ Planner* │                             │            │
└──────────┴─────────────────────────────┴────────────┘
   * = visible, disabled, "soon" — future IA, not built this week
```

**Signature element:** The `improve()` sequence — progress fill → stats counting in (relationships found / concepts merged / duplicates removed) → completion checkmark → the *same question, visibly better answer* appearing below it. This is the one moment we spend all our boldness on. Per the brief's own closing instruction ("optimize for making persistent evolving memory understandable within 30 seconds"), this sequence **is** the 30 seconds. Everything else in the UI is deliberately quieter so this doesn't have to compete for attention.

**Self-critique pass:** Original draft had glow effects on every card and chip — cut to one glow source (the brand mark + active specialist ring) per the "remove one accessory" principle; scattered glow reads as decoration, one consistent glow source reads as "this is where the energy is."

---

## 2. Design Tokens

```css
:root {
  /* Surface */
  --bg-0: #0A0B0E;   /* app void */
  --bg-1: #111319;   /* cards, bubbles, panel body */
  --bg-2: #161922;   /* hover states */
  --bg-3: #1C2029;   /* active/selected states, user bubbles */

  /* Borders */
  --border: rgba(255,255,255,0.07);
  --border-strong: rgba(255,255,255,0.14);

  /* Text */
  --text-0: #F2F3F5;  /* primary */
  --text-1: #A8ADB8;  /* secondary */
  --text-2: #6E7380;  /* tertiary / system labels */

  /* Accent */
  --accent: #4D8DFF;
  --accent-glow: rgba(77,141,255,0.35);
  --purple: #9B7CFF;   /* relationships / cross-domain only */
  --emerald: #34D399;  /* success / live / high confidence */
  --amber: #F2B544;    /* pre-improve / shallow state only */

  /* Type */
  --font-display: 'Inter', -apple-system, sans-serif;
  --font-body: 'Inter', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', monospace;

  /* Radius */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 18px;

  /* Motion */
  --ease: cubic-bezier(0.16, 1, 0.3, 1);
}
```

**Type scale**

| Role | Size | Weight | Family | Usage |
|---|---|---|---|---|
| Screen title | 19px | 600 | display | Workspace header h1 only |
| Body / chat | 13.8px | 400–500 | body | Messages, cards |
| Label / nav | 13.5px | 500 | body | Nav items, specialist labels |
| Caption | 11–12.5px | 500–600 | body | Crumbs, goals, section titles |
| System / mono | 9.5–11px | 500–600 | mono | Timestamps, trace chips, stats |

**Spacing scale:** 4 / 6 / 8 / 10 / 12 / 14 / 16 / 18 / 20 / 24 / 28px — no arbitrary values outside this set.

---

## 3. Information Architecture (this week's scope only)

```
MemoryOS
├── Workspace          ← CORE — chat-as-reasoning, default landing screen
│   ├── Specialist Switcher (Developer / Learning live, Research / Planner locked)
│   ├── Message thread (shallow + deep answer states)
│   ├── improve() trigger + animated sequence
│   └── Composer
├── Memory Panel (always docked, right side)
│   ├── Graph tab     ← CORE — small live graph viz
│   └── Timeline tab  ← CORE — story-of-memory log
├── Projects           ← FUTURE — nav item visible, disabled, "SOON" tag
└── Settings           ← FUTURE — nav item visible, disabled, "SOON" tag
```

Note: the original brief's IA (Memory / Timeline / Workspace / Graph / Projects / Settings as six equal nav destinations) is the **post-hackathon** IA. This week, Graph and Timeline are **tabs inside the docked Memory Panel**, not separate full-screen destinations — this was a deliberate scope cut (see PRD §9) to avoid building navigation infrastructure for views that don't yet have enough distinct content to justify a full screen each. When Research/Planner ship for real, Graph and Timeline likely get promoted to full nav destinations, matching the original brief exactly.

---

## 4. Screen List (built this week)

1. **Workspace — Developer specialist** (default view)
2. **Workspace — Learning specialist** (same shell, swapped header/context, instant transform)
3. **Memory Panel — Graph tab**
4. **Memory Panel — Timeline tab**
5. **`improve()` in-flow sequence** (not a separate screen — an animated state within Workspace)

Out of scope this week: Projects screen, Settings screen, Research/Planner working workspaces, full-screen Graph explorer, full-screen Timeline.

---

## 5. Component System (React, for the future Next.js rebuild)

These are written as standalone, dependency-light components using the token system above via CSS variables + Tailwind-style utility classes where natural. They mirror the working HTML prototype's behavior exactly, so the prototype can be treated as the interaction spec when porting.

### 5.1 SpecialistSwitcher

```jsx
import { useState } from "react";

const SPECIALISTS = [
  { id: "developer", label: "Developer", status: "live" },
  { id: "learning", label: "Learning", status: "live" },
  { id: "research", label: "Research", status: "soon" },
  { id: "planner", label: "Planner", status: "soon" },
];

export default function SpecialistSwitcher({ active, onChange }) {
  return (
    <div className="flex flex-col gap-1.5 px-1">
      {SPECIALISTS.map((s) => {
        const isActive = s.id === active;
        const isLocked = s.status === "soon";
        return (
          <button
            key={s.id}
            disabled={isLocked}
            onClick={() => !isLocked && onChange(s.id)}
            className={`flex items-center gap-2.5 px-2.5 py-2 rounded-xl border text-left transition-all duration-200
              ${isActive ? "border-[#4D8DFF] bg-gradient-to-br from-[rgba(77,141,255,0.10)] to-[rgba(155,124,255,0.05)]" : "border-white/[0.07] bg-[#111319]"}
              ${isLocked ? "opacity-45 cursor-default" : "cursor-pointer hover:border-white/[0.14]"}`}
          >
            <span
              className={`w-2 h-2 rounded-full border-2 transition-all duration-200
                ${isActive ? "border-[#4D8DFF] bg-[#4D8DFF] shadow-[0_0_10px_rgba(77,141,255,0.35)]" : "border-[#6E7380]"}`}
            />
            <span className="text-[13px] font-semibold text-[#F2F3F5]">{s.label}</span>
            <span className="ml-auto text-[10.5px] font-mono text-[#6E7380]">{s.status}</span>
          </button>
        );
      })}
    </div>
  );
}
```

### 5.2 ImproveSequence

```jsx
import { useState, useEffect } from "react";

export default function ImproveSequence({ onComplete }) {
  const [stage, setStage] = useState(0); // 0 idle, 1 running, 2 done

  const run = () => {
    if (stage !== 0) return;
    setStage(1);
    setTimeout(() => setStage(2), 2200);
    setTimeout(() => onComplete?.(), 3300);
  };

  const stats = [
    { num: 4, label: "Relationships found" },
    { num: 2, label: "Concepts merged" },
    { num: 1, label: "Duplicate removed" },
  ];

  if (stage === 0) {
    return (
      <button
        onClick={run}
        className="flex items-center gap-1.5 bg-[#161922] border border-white/[0.14] text-[#A8ADB8] text-xs font-semibold px-3.5 py-2 rounded-xl hover:text-[#4D8DFF] hover:border-[#4D8DFF] transition-colors"
      >
        Run improve()
      </button>
    );
  }

  return (
    <div className="w-full max-w-[480px] mx-auto bg-gradient-to-br from-[rgba(77,141,255,0.08)] to-[rgba(155,124,255,0.06)] border border-[rgba(77,141,255,0.25)] rounded-[18px] p-4 px-5">
      <div className="flex items-center gap-2 text-[13px] font-semibold mb-2.5">
        {stage === 1 && (
          <span className="w-3 h-3 rounded-full border-2 border-white/[0.14] border-t-[#4D8DFF] animate-spin" />
        )}
        <span>{stage === 1 ? "Memory improving…" : "Memory evolution complete"}</span>
      </div>
      <div className="h-1 rounded-full bg-[#1C2029] overflow-hidden mb-3">
        <div
          className="h-full rounded-full bg-gradient-to-r from-[#4D8DFF] to-[#9B7CFF] transition-all duration-[2200ms]"
          style={{ width: stage >= 1 ? "100%" : "0%" }}
        />
      </div>
      <div className="grid grid-cols-3 gap-2">
        {stats.map((s, i) => (
          <div
            key={s.label}
            className={`text-center py-2 px-1 rounded-lg bg-[#111319] border border-white/[0.07] transition-all duration-400
              ${stage >= 1 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-1"}`}
            style={{ transitionDelay: `${600 + i * 400}ms` }}
          >
            <div className="font-mono text-[17px] font-semibold text-[#F2F3F5]">{s.num}</div>
            <div className="text-[9.5px] text-[#6E7380] uppercase tracking-wide mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>
      {stage === 2 && (
        <div className="text-center text-[11.5px] text-[#34D399] font-semibold mt-3">
          ✓ Memory evolution complete
        </div>
      )}
    </div>
  );
}
```

### 5.3 RecallTrace (the "why the AI knows this" chip row)

```jsx
export default function RecallTrace({ hops, mode, label }) {
  return (
    <div className="flex gap-1.5 flex-wrap mt-1">
      <span className="text-[10px] font-mono px-2 py-0.5 rounded-full border border-white/[0.07] bg-[#161922] text-[#A8ADB8] flex items-center gap-1.5">
        <span className="w-1.5 h-1.5 rounded-full bg-[#9B7CFF]" />
        {hops} hop{hops > 1 ? "s" : ""} {label ? `· ${label}` : ""}
      </span>
      {mode && (
        <span className="text-[10px] font-mono px-2 py-0.5 rounded-full border border-white/[0.07] bg-[#161922] text-[#A8ADB8]">
          {mode}
        </span>
      )}
    </div>
  );
}
```

### 5.4 MemoryCard

```jsx
export default function MemoryCard({ fact, confidence, source, relationships }) {
  const confLevel = confidence >= 0.85 ? "high" : "med";
  const confColor =
    confLevel === "high"
      ? "bg-[rgba(52,211,153,0.12)] text-[#34D399]"
      : "bg-[rgba(242,181,68,0.12)] text-[#F2B544]";
  const srcColor = source === "learning" ? "bg-[#9B7CFF]" : "bg-[#4D8DFF]";

  return (
    <div className="border border-white/[0.07] rounded-xl p-3 px-3.5 mb-2 bg-[#111319] hover:border-white/[0.14] transition-colors">
      <div className="flex justify-between items-start gap-2">
        <div className="text-[12.5px] text-[#F2F3F5] font-medium leading-snug">{fact}</div>
        <div className={`flex-shrink-0 text-[9.5px] font-mono px-1.5 py-0.5 rounded-full font-semibold ${confColor}`}>
          {confidence.toFixed(2)}
        </div>
      </div>
      <div className="flex items-center gap-2.5 mt-2 text-[10px] text-[#6E7380] font-mono">
        <span className="flex items-center gap-1 px-1.5 py-0.5 rounded-md bg-[#161922] border border-white/[0.07]">
          <span className={`w-1.5 h-1.5 rounded-full ${srcColor}`} />
          {source}
        </span>
        <span>{relationships} relationships</span>
      </div>
    </div>
  );
}
```

### 5.5 TimelineItem

```jsx
export default function TimelineItem({ title, sub, time, faded }) {
  return (
    <div className="relative pl-4 pb-5">
      <span
        className={`absolute -left-[1px] top-0.5 w-2.5 h-2.5 rounded-full bg-[#0A0B0E] border-2
          ${faded ? "border-[#6E7380]" : "border-[#4D8DFF]"}`}
      />
      <div className="text-[12.5px] font-semibold text-[#F2F3F5]">{title}</div>
      <div className="text-[11px] text-[#A8ADB8] mt-0.5 leading-snug">{sub}</div>
      <div className="text-[9.5px] text-[#6E7380] font-mono mt-1">{time}</div>
    </div>
  );
}
```

---

## 6. Mobile Considerations

The three-pane shell collapses to a **single pane** below 980px:
- Nav and Memory Panel become slide-over sheets, triggered by icon buttons in the topbar (not always-visible — screen real estate forces a choice the desktop version avoids).
- The Memory Panel's Graph tab becomes a tap-to-expand card rather than a permanently visible mini-viz, since a meaningful graph render needs more than a phone-width sliver to read as "alive" rather than as noise.
- `improve()` sequence behavior is unchanged — it's the signature moment and should not be simplified away on mobile.
- Specialist switcher becomes a horizontal scrollable pill row pinned under the topbar, not a vertical list.

This is a "should work, not a priority" consideration for hackathon week — the demo video will be recorded on desktop. Build mobile responsiveness only if Core + Should tiers (per PRD) are done with time remaining.

---

## 7. Accessibility Floor

- All interactive elements have visible `:focus-visible` outlines (electric blue, 2px, 2px offset) — already in the prototype's base styles.
- `prefers-reduced-motion` respected globally — the `improve()` sequence and graph float animation both degrade to instant/static states.
- Color is never the only signal: confidence badges carry both color and numeric value; source tags carry both color dot and text label.

---

## 8. Why Streamlit + this CSS, not React, this week

The working prototype (`prototype.html`) is plain HTML/CSS/JS so it can be embedded directly into the Streamlit app via `st.components.v1.html(open('prototype.html').read(), height=900)` with zero build tooling. The React components above are **not used this week** — they exist so that when MemoryOS is rebuilt as a real Next.js product post-hackathon, the interaction design doesn't have to be reinvented, only re-implemented in the target stack. Treat `prototype.html` as the source of truth for behavior/timing; treat this section as the source of truth for component boundaries when that rebuild happens.

---

## 9. Deferred (full future IA, for reference only — not designed this week)

Per the original brief: Memory, Timeline, Workspace, Graph, Projects, Settings as six equal top-level nav destinations; full Settings screen; full Projects screen (multi-project memory scoping); Research and Planner as fully built specialist workspaces with their own recall lenses and write triggers; a full-screen, pannable/zoomable graph explorer (this week's graph is a small preview only, per brief's own instruction that it should be "small, elegant, expandable" — expansion itself is future work). These are intentionally **not specced in detail here** — see PRD §3 and §7.3–7.4 for why, and revisit this file when that build begins.
