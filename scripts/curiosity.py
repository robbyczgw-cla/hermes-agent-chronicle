from __future__ import annotations
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from common import get_support_file_path


def curiosity_path() -> Path:
    return get_support_file_path("curiosity.md")


def load_lines() -> List[str]:
    path = curiosity_path()
    if not path.exists():
        return ["# Curiosity Backlog", ""]
    return path.read_text(encoding="utf-8").splitlines()


def save_lines(lines: List[str]) -> None:
    curiosity_path().write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_items() -> List[Dict[str, str]]:
    path = curiosity_path()
    if not path.exists():
        return []
    items: List[Dict[str, str]] = []
    current: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if current:
                items.append(current)
            current = {"title": line[3:].strip()}
        elif line.startswith("- "):
            key, _, value = line[2:].partition(":")
            current[key.lower().strip()] = value.strip()
    if current:
        items.append(current)
    return items


def add_item(question: str, priority: str) -> None:
    lines = load_lines()
    lines.extend(
        [
            f"## {question}",
            f"- Added: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            f"- Priority: {priority}",
            "- Status: open",
            "",
        ]
    )
    save_lines(lines)
    print(f"Added curiosity item to {curiosity_path()}")


def list_items(status: str) -> None:
    items = parse_items()
    filtered = []
    for item in items:
        item_status = item.get("status", "open")
        if status == "all" or item_status == status:
            filtered.append(item)
    if not filtered:
        print("No curiosity items found.")
        return
    for item in filtered:
        print(f"- {item['title']} [{item.get('status', 'open')}] priority={item.get('priority', 'medium')}")


def mark_done(topic: str) -> None:
    lines = load_lines()
    updated: List[str] = []
    in_target = False
    found = False
    for line in lines:
        if line.startswith("## "):
            in_target = line[3:].strip() == topic
            if in_target:
                found = True
        if in_target and line.lower().startswith("- status:"):
            updated.append("- Status: resolved")
            continue
        updated.append(line)
    if not found:
        print(f'No curiosity item matched "{topic}".')
        return
    save_lines(updated)
    print(f'Marked "{topic}" as resolved.')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Agent Chronicle curiosity backlog.")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a curiosity item.")
    add_parser.add_argument("question", help="Question or topic.")
    add_parser.add_argument(
        "--priority",
        choices=("high", "medium", "low"),
        default="medium",
        help="Priority level.",
    )

    list_parser = subparsers.add_parser("list", help="List curiosity items.")
    list_parser.add_argument(
        "--status",
        choices=("open", "resolved", "all"),
        default="open",
        help="Status filter.",
    )

    done_parser = subparsers.add_parser("done", help="Mark a curiosity item resolved.")
    done_parser.add_argument("topic", help="Exact topic title to resolve.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "add":
        add_item(args.question, args.priority)
    elif args.command == "list":
        list_items(args.status)
    elif args.command == "done":
        mark_done(args.topic)
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
