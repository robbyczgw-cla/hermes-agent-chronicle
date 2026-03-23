# Agent Chronicle for Hermes

Agent Chronicle is a Hermes-native AI journaling tool. It writes daily entries from the agent's own perspective and keeps supporting logs for memorable quotes, open curiosities, decisions, relationship evolution, and memory integration.

## Features

- Daily diary generation through the local Hermes Agent API at `http://localhost:8642/v1/chat/completions`
- Entry structure covering summary, projects, wins, frustrations, learnings, emotional state, notable interactions, and tomorrow focus
- Quote Hall of Fame, Curiosity Backlog, Decision Archaeology, and Relationship Evolution modules
- Optional one-line memory integration appended to `~/.hermes/memory.md`
- Markdown, HTML, and PDF export of recent entries

## Requirements

- Python 3.8+
- `requests`
- `pandoc` for PDF or HTML export

Install the only external dependency:

```bash
python -m pip install requests
```

## Storage

By default, Agent Chronicle stores data in `~/.hermes/chronicle`.

- Config: `~/.hermes/chronicle/config.json`
- Daily entries: `~/.hermes/chronicle/YYYY-MM-DD.md`
- Quotes: `~/.hermes/chronicle/quotes.md`
- Curiosity backlog: `~/.hermes/chronicle/curiosity.md`
- Decisions: `~/.hermes/chronicle/decisions.md`
- Relationship evolution: `~/.hermes/chronicle/relationship.md`

Set `HERMES_CHRONICLE_DIR` to override the storage directory.

## Setup

Run the interactive setup wizard:

```bash
python scripts/setup.py
```

The wizard prompts for:

- Privacy level: `private`, `shareable`, or `public`
- Diary directory
- Memory integration on or off
- Preferred Hermes model

## Environment

Copy values from `.env.template` into your shell environment as needed:

```bash
export HERMES_CHRONICLE_DIR=~/.hermes/chronicle
export HERMES_CHRONICLE_MODEL=anthropic/claude-sonnet-4-6
export HERMES_API_KEY=your-token-if-needed
```

`HERMES_API_KEY` is optional. If it is not set, no `Authorization` header is sent.

## Usage

Generate today's entry:

```bash
python scripts/generate.py
```

Interactive generation:

```bash
python scripts/generate.py --interactive
```

Generate from a file:

```bash
python scripts/generate.py --from-file session-context.md
```

Inspect entries:

```bash
python scripts/generate.py --view
python scripts/generate.py --list
```

Work with quotes:

```bash
python scripts/quotes.py add "Precision matters more than speed when the interface is brittle." --source "internal reflection"
python scripts/quotes.py list
python scripts/quotes.py random
```

Work with curiosities:

```bash
python scripts/curiosity.py add "How should long-running agent memory be summarized?" --priority high
python scripts/curiosity.py list --status all
python scripts/curiosity.py done "How should long-running agent memory be summarized?"
```

Work with decisions:

```bash
python scripts/decisions.py add "Use plain markdown for support files" --reasoning "Keeps the data easy to inspect and edit"
python scripts/decisions.py list --days 14
python scripts/decisions.py revisit
```

Work with relationship evolution:

```bash
python scripts/relationship.py update "The interaction pattern became more collaborative after tighter feedback loops."
python scripts/relationship.py view
```

Export recent entries:

```bash
python scripts/export.py --format markdown --days 7 --output exports/chronicle.md
python scripts/export.py --format html --days 7 --output exports/chronicle.html
python scripts/export.py --format pdf --days 7 --output exports/chronicle.pdf
```

For `html` and `pdf`, the exporter calls `pandoc --sandbox` and prints a clear message if `pandoc` is unavailable.

## Privacy

The configured privacy level is passed into generation prompts so the resulting entry can stay private, selectively shareable, or public-ready.

## Templates

- `templates/daily.md`
- `templates/weekly.md`

These templates are included for customization and downstream tooling.
