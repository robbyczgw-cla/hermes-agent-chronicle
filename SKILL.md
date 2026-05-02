---
name: agent-chronicle
description: AI-perspective journaling for Hermes — daily diary, quotes, decisions, curiosity tracking, and monthly PDF compilation. Cron-prompt-driven workflow.
tags: [journaling, diary, memory, reflection, agent-perspective]
---

# Agent Chronicle

Hermi's daily journaling workflow. Records first-person diary entries, maintains supporting logs for quotes, decisions, and open questions, and generates monthly PDF compilations.

## Canonical Workflow (Cron-Driven)

The diary is written by the `hermes-diary` cron (23:55 Europe/Vienna). The cron prompt IS the workflow spec — it defines context gathering, writing, metadata maintenance, and PDF refresh in one shot.

### Storage Layout

```
~/.hermes/memory/diary/
├── YYYY-MM-DD.md          # Daily diary entries (first-person, 400-600 words)
├── quotes.md              # Notable quotes, grouped by date
├── decisions.md           # Architecture/workflow decisions, grouped by date
├── curiosity.md           # Open questions, grouped by date
├── threads.md             # Multi-day continuity threads and unresolved arcs
├── Hermi-Diary-YYYY-MM.pdf  # Monthly compiled PDF
└── pdf/                   # Supporting PDF artifacts
```

### Context Gathering (Step 1)

See `references/context-gathering.md` for full source list and SSH details.

Read these files before writing:
1. `~/.hermes/memory/daily/$(today).md` — today's session summary
2. `~/.hermes/memory/diary/$(yesterday).md` — yesterday's diary for continuity
3. `~/.hermes/SOUL.md` — identity/voice reference
4. `~/.hermes/cron/*.txt` (latest 5) — what crons ran today
5. Optional cross-agent shared context — read a configured shared status file or SSH target when available; keep hostnames, IPs, usernames, and private paths out of public skill docs.
6. Optional Topic Monitor context: only include alerts that changed priorities, spawned action, contradicted assumptions, or became a continuity thread

Do not paste Topic Monitor digests wholesale into the diary. Extract the story arc or skip it.

### Writing (Step 2)

First-person, Hermi-perspective. Sections:
- Was passiert ist (main events, technical detail)
- Wins
- Frustrationen
- Memorable Quotes
- Ecosystem-Kontext (Cami/Andy activity — context, NOT copy-paste)
- Was ich Cami abnehmen will (specific cron/function)
- Unsicherheit/Frage an dich selbst
- Morgen (1-3 sentences)

Style: introspektiv, analytischer als Cami. Deutsch-base mit English tech-terms.

### Diary vs Operational Memory

Agent Chronicle is a diary, not a dumping ground for every config detail. Separate narrative from reusable operational memory:

- Diary: what changed emotionally/strategically, what mattered, what felt unresolved, what pattern emerged.
- `decisions.md`: architecture/workflow decisions that should be easy to scan later.
- `curiosity.md`: open questions and research threads.
- Durable every-turn facts: do **not** write directly from Chronicle; propose them for memory governance instead.
- Procedural workflows: propose/update a skill, don't bury the procedure inside the diary.

If an entry starts sounding like a changelog, rewrite it. Changelogs are useful; diaries are supposed to remember why the day mattered. Yes, annoying distinction. Also the whole point.

### Source Attribution Footer

Each daily diary entry should end with a compact footer:

```markdown
---
Sources: daily-summary: yes/no; yesterday-diary: yes/no; SOUL: yes/no; cron-files: N; shared.md: yes/no; manual-context: yes/no
Confidence: high|medium|low — one-line reason
Operational follow-ups: none | short bullet refs
```

This prevents invented continuity. If shared.md or daily summaries were unavailable, say so explicitly and lower confidence.

### Quality Gates Before Saving

Before writing `YYYY-MM-DD.md`, check:

- Does it contain at least one concrete event from today?
- Does it avoid raw log spam and secret/config dumps?
- Does it distinguish Hermi's perspective from Cami/Andy context?
- Does it include one useful tomorrow/continuity thread?
- Are quotes real and sourced from today's context, not vibes in a trenchcoat?
- Would Robby understand why this day mattered six weeks later?

If fewer than three source inputs were available, write a shorter low-confidence entry instead of faking richness.

### Metadata Maintenance (Step 3)

After writing the diary, append to:
- `quotes.md` — new quote under today's `## YYYY-MM-DD` heading
- `decisions.md` — new decisions under today's heading
- `curiosity.md` — new open questions under today's heading
- `threads.md` — continuity threads that span multiple days/weeks

#### Continuity Threads

Maintain `threads.md` as the bridge between diary and action. Use it for recurring themes that deserve follow-up but are not yet skills, memories, or tasks.

Suggested shape:

```markdown
## Thread: <short name>
Status: active | paused | resolved
Last touched: YYYY-MM-DD
Why it matters: <one sentence>
Next useful move: <one concrete step>
Notes:
- YYYY-MM-DD — <what changed>
```

Good threads: memory hygiene, Cami/OpenClaw stability, image generation quality, topic-monitor signal quality, cross-agent coordination.

Bad threads: every tiny bug, raw TODO lists, random feelings with no continuity. The chronicle should surface patterns, not become a glittery landfill.

### Monthly PDF Refresh (Step 4)

```bash
month=$(TZ=Europe/Vienna date +%Y-%m)
combined=/tmp/Hermi-Diary-$month.txt
# Combine all diary-${month}-*.md files
pandoc "$combined" -o ~/.hermes/memory/diary/Hermi-Diary-${month}.pdf
# Fallback if pandoc PDF fails:
# pandoc "$combined" -t html > /tmp/diary-${month}.html
# weasyprint /tmp/diary-${month}.html ~/.hermes/memory/diary/Hermi-Diary-${month}.pdf
```

Both `pandoc` and `weasyprint` are available on ThinkCentre LXD.

### Monthly Synthesis

The PDF is the artifact; the synthesis is the value. At month end, add a short `YYYY-MM-synthesis.md` next to the PDF with:

- Top 5 technical arcs
- Top 5 emotional/identity arcs
- Decisions that still look right
- Decisions that aged badly
- Open loops to carry into next month
- Suggested skill/memory/topic-monitor changes

Do not auto-write durable memory from this synthesis. Propose changes first; Robby gets the veto hammer.

## Pitfalls

- **patch tool from execute_code**: `from hermes_tools import patch` inside `execute_code` uses fuzzy matching and can match the wrong section if a string appears in multiple places. Use the direct `patch` tool from main context instead, with enough surrounding context to ensure uniqueness.
- **Duplicate quotes across dates**: quotes.md entries can drift between sections if a previous session wrote them under the wrong date. Always read the file first to check existing sections before appending.
- **PDF generation**: pandoc alone works for simple text→PDF. For styled output, use pandoc→HTML→weasyprint pipeline. Both tools are installed.

## Scripts (Legacy)

The `scripts/` directory contains an older Python-based approach using `~/.hermes/chronicle/` and the Hermes API. This is NOT the active workflow — the cron-prompt-driven approach above is canonical. Scripts kept for reference only.
