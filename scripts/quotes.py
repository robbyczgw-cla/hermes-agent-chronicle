from __future__ import annotations

import argparse
import random
from datetime import datetime
from pathlib import Path
from typing import List

from common import get_support_file_path


def quotes_path() -> Path:
    return get_support_file_path("quotes.md")


def load_lines() -> List[str]:
    path = quotes_path()
    if not path.exists():
        return ["# Quote Hall of Fame", ""]
    return path.read_text(encoding="utf-8").splitlines()


def save_lines(lines: List[str]) -> None:
    quotes_path().write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def add_quote(text: str, context: str | None, source: str | None) -> None:
    lines = load_lines()
    lines.extend(
        [
            f"## {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            f"- Quote: {text}",
            f"- Context: {context or 'n/a'}",
            f"- Source: {source or 'n/a'}",
            "",
        ]
    )
    save_lines(lines)
    print(f"Added quote to {quotes_path()}")


def list_quotes() -> None:
    path = quotes_path()
    if not path.exists():
        print("No quotes recorded.")
        return
    print(path.read_text(encoding="utf-8").strip())


def random_quote() -> None:
    path = quotes_path()
    if not path.exists():
        print("No quotes recorded.")
        return
    blocks = [block.strip() for block in path.read_text(encoding="utf-8").split("\n## ") if "Quote:" in block]
    if not blocks:
        print("No quotes recorded.")
        return
    block = random.choice(blocks)
    if not block.startswith("## "):
        block = "## " + block
    print(block)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Agent Chronicle quotes.")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a quote.")
    add_parser.add_argument("text", help="Quote text.")
    add_parser.add_argument("--context", help="Optional context.")
    add_parser.add_argument("--source", help="Optional source.")

    subparsers.add_parser("list", help="List quotes.")
    subparsers.add_parser("random", help="Show a random quote.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "add":
        add_quote(args.text, args.context, args.source)
    elif args.command == "list":
        list_quotes()
    elif args.command == "random":
        random_quote()
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
