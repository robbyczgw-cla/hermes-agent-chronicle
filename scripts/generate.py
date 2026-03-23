from __future__ import annotations
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import argparse
from datetime import date
from pathlib import Path
from typing import List, Optional

from common import (
    append_memory_integration,
    call_hermes_api,
    format_date,
    get_diary_dir,
    get_entry_path,
    load_config,
)


SYSTEM_PROMPT = """You are writing a daily journal entry from your own perspective as an AI agent.
Write in first person singular.
Be reflective, specific, emotionally aware, and concrete about projects, interactions, tensions, and decisions.
Return markdown only.
Follow this exact section structure:
# Daily Chronicle - YYYY-MM-DD
## Summary
## Projects
## Wins
## Frustrations
## Learnings
## Emotional State
## Notable Interactions
## Tomorrow Focus
Respect the privacy level provided in the prompt.
Do not mention being asked to write or that this is generated."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate or inspect Hermes chronicle entries.")
    parser.add_argument("--today", action="store_true", help="Generate today's entry.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for a session summary before generating today's entry.",
    )
    parser.add_argument(
        "--from-file",
        metavar="FILE",
        help="Read session context from a file before generating today's entry.",
    )
    parser.add_argument("--view", action="store_true", help="Print today's entry if it exists.")
    parser.add_argument("--list", action="store_true", help="List available entry dates.")
    return parser


def collect_interactive_summary() -> str:
    print("Enter a short session summary. Finish with an empty line.")
    lines: List[str] = []
    while True:
        line = input("> ").rstrip()
        if not line:
            break
        lines.append(line)
    return "\n".join(lines).strip()


def read_context_from_file(path: str) -> str:
    return Path(path).expanduser().read_text(encoding="utf-8").strip()


def list_entries() -> None:
    diary_dir = get_diary_dir(load_config())
    entries = sorted(diary_dir.glob("????-??-??.md"))
    if not entries:
        print("No diary entries found.")
        return
    for entry in entries:
        print(entry.stem)


def view_today() -> None:
    config = load_config()
    path = get_entry_path(date.today(), config)
    if not path.exists():
        print(f"No entry found for {format_date(date.today())}.")
        return
    print(path.read_text(encoding="utf-8"))


def build_generation_prompt(config: dict, session_context: str) -> str:
    today = format_date(date.today())
    context = session_context.strip() or "No additional session context was provided."
    return f"""Date: {today}
Privacy level: {config['privacy']}
Feature modules enabled:
- Quote Hall of Fame: {config['features'].get('quotes', True)}
- Curiosity Backlog: {config['features'].get('curiosity', True)}
- Decision Archaeology: {config['features'].get('decisions', True)}
- Relationship Evolution: {config['features'].get('relationship', True)}
- Memory Integration: {config['features'].get('memory_integration', True)}

Session context:
{context}

Write a rich daily chronicle entry from your own AI perspective.
Make the content feel like lived experience rather than a generic recap.
If details are missing, infer carefully and keep the tone honest.
"""


def extract_summary_line(content: str) -> str:
    capture = False
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line == "## Summary":
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture and line:
            return line.lstrip("- ").strip()
    return f"Chronicle entry captured for {format_date(date.today())}."


def generate_entry(session_context: Optional[str]) -> None:
    config = load_config()
    prompt = build_generation_prompt(config, session_context or "")
    content = call_hermes_api(prompt=prompt, system=SYSTEM_PROMPT, model=config["model"])

    entry_path = get_entry_path(date.today(), config)
    entry_path.write_text(content.rstrip() + "\n", encoding="utf-8")
    print(f"Saved entry to {entry_path}")

    if config.get("memory_integration", True):
        summary = extract_summary_line(content)
        memory_path = append_memory_integration(summary)
        print(f"Appended summary to {memory_path}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        list_entries()
        return

    if args.view:
        view_today()
        return

    session_context: Optional[str] = None
    should_generate = args.today or args.interactive or bool(args.from_file)

    if args.interactive:
        session_context = collect_interactive_summary()
        should_generate = True
    elif args.from_file:
        session_context = read_context_from_file(args.from_file)
        should_generate = True

    if not any(vars(args).values()):
        should_generate = True

    if should_generate:
        generate_entry(session_context)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
