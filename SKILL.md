---
name: agent-chronicle
description: AI-perspective journaling for Hermes — capture experiences, quotes, curiosities, decisions and relationship evolution. Generates rich diary entries via the Hermes API.
tags: [journaling, diary, memory, reflection, agent-perspective]
---

# Agent Chronicle

Agent Chronicle is a Hermes-native journaling workflow for AI agents. It records daily entries from the agent's own perspective and maintains supporting logs for memorable quotes, curiosity threads, decisions, and relationship evolution.

## Setup

Run:

```bash
python scripts/setup.py
```

The wizard saves configuration to `~/.hermes/chronicle/config.json` unless `HERMES_CHRONICLE_DIR` is set.

## Environment Variables

- `HERMES_CHRONICLE_DIR`: Override the chronicle storage directory. Default: `~/.hermes/chronicle`
- `HERMES_CHRONICLE_MODEL`: Default model for generation. Default: `anthropic/claude-sonnet-4-6`
- `HERMES_API_KEY`: Optional bearer token for the local Hermes API

## Daily Use

Generate today's entry:

```bash
python scripts/generate.py
```

Interactive generation:

```bash
python scripts/generate.py --interactive
```

Generate from a session file:

```bash
python scripts/generate.py --from-file ./session-notes.md
```

View or list entries:

```bash
python scripts/generate.py --view
python scripts/generate.py --list
```

## Supporting Modules

Quotes:

```bash
python scripts/quotes.py add "I should verify that assumption." --context "debugging the export path"
python scripts/quotes.py list
python scripts/quotes.py random
```

Curiosity:

```bash
python scripts/curiosity.py add "What pattern best captures recurring user intent?" --priority high
python scripts/curiosity.py list --status open
python scripts/curiosity.py done "What pattern best captures recurring user intent?"
```

Decisions:

```bash
python scripts/decisions.py add "Switch chronicle storage to ~/.hermes/chronicle" --reasoning "Hermes tools should keep state outside the repo"
python scripts/decisions.py list --days 30
python scripts/decisions.py revisit
```

Relationship evolution:

```bash
python scripts/relationship.py update "Trust increased after several precise implementation passes."
python scripts/relationship.py view
```

## Export

Markdown export:

```bash
python scripts/export.py --format markdown --days 7 --output exports/weekly.md
```

PDF or HTML export requires `pandoc` and uses `--sandbox`:

```bash
python scripts/export.py --format pdf --days 7 --output exports/weekly.pdf
python scripts/export.py --format html --days 7 --output exports/weekly.html
```

## Cron Examples

Daily generation at 23:55 UTC:

```cron
55 23 * * * cd /home/hermes/hermes-agent-chronicle && /usr/bin/python3 scripts/generate.py >> /tmp/agent-chronicle.log 2>&1
```

Daily generation with explicit model override:

```cron
55 23 * * * cd /home/hermes/hermes-agent-chronicle && HERMES_CHRONICLE_MODEL=anthropic/claude-sonnet-4-6 /usr/bin/python3 scripts/generate.py >> /tmp/agent-chronicle.log 2>&1
```
