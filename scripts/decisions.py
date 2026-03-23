from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List

from common import format_date, get_support_file_path, parse_date


def decisions_path() -> Path:
    return get_support_file_path("decisions.md")


def load_lines() -> List[str]:
    path = decisions_path()
    if not path.exists():
        return ["# Decision Archaeology", ""]
    return path.read_text(encoding="utf-8").splitlines()


def save_lines(lines: List[str]) -> None:
    decisions_path().write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_decisions() -> List[Dict[str, str]]:
    path = decisions_path()
    if not path.exists():
        return []
    decisions: List[Dict[str, str]] = []
    current: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if current:
                decisions.append(current)
            current = {"title": line[3:].strip()}
        elif line.startswith("- "):
            key, _, value = line[2:].partition(":")
            current[key.lower().strip()] = value.strip()
    if current:
        decisions.append(current)
    return decisions


def add_decision(decision: str, reasoning: str, outcome: str | None) -> None:
    lines = load_lines()
    lines.extend(
        [
            f"## {decision}",
            f"- Date: {format_date(date.today())}",
            f"- Reasoning: {reasoning}",
            f"- Outcome: {outcome or 'pending'}",
            "- Reviewed: no",
            "- Reflection: pending",
            "",
        ]
    )
    save_lines(lines)
    print(f"Added decision to {decisions_path()}")


def list_decisions(days: int | None) -> None:
    items = parse_decisions()
    if days is not None:
        cutoff = date.today() - timedelta(days=days)
        items = [item for item in items if parse_date(item["date"]) >= cutoff]
    if not items:
        print("No decisions found.")
        return
    for item in items:
        print(
            f"- {item['date']} | {item['title']} | reviewed={item.get('reviewed', 'no')} | outcome={item.get('outcome', 'pending')}"
        )


def revisit_decisions() -> None:
    items = parse_decisions()
    pending = [item for item in items if item.get("reviewed", "no").lower() != "yes"]
    if not pending:
        print("No unreviewed decisions found.")
        return

    target = pending[0]
    print(f"Decision: {target['title']}")
    print(f"Reasoning: {target.get('reasoning', 'n/a')}")
    print(f"Outcome: {target.get('outcome', 'pending')}")
    reflection = input("Reflection: ").strip()
    if not reflection:
        print("No reflection entered. Nothing changed.")
        return

    lines = load_lines()
    updated: List[str] = []
    in_target = False
    for line in lines:
        if line.startswith("## "):
            in_target = line[3:].strip() == target["title"]
        if in_target and line.lower().startswith("- reviewed:"):
            updated.append("- Reviewed: yes")
            continue
        if in_target and line.lower().startswith("- reflection:"):
            updated.append(f"- Reflection: {reflection}")
            continue
        updated.append(line)

    save_lines(updated)
    print(f'Reviewed decision "{target["title"]}".')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Agent Chronicle decisions.")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a decision.")
    add_parser.add_argument("decision", help="Decision description.")
    add_parser.add_argument("--reasoning", required=True, help="Reasoning behind the decision.")
    add_parser.add_argument("--outcome", help="Optional outcome.")

    list_parser = subparsers.add_parser("list", help="List decisions.")
    list_parser.add_argument("--days", type=int, help="Filter to recent decisions.")

    subparsers.add_parser("revisit", help="Reflect on the oldest unreviewed decision.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "add":
        add_decision(args.decision, args.reasoning, args.outcome)
    elif args.command == "list":
        list_decisions(args.days)
    elif args.command == "revisit":
        revisit_decisions()
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
