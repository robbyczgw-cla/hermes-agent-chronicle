from __future__ import annotations
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import argparse
from datetime import datetime
from pathlib import Path

from common import get_support_file_path


def relationship_path() -> Path:
    return get_support_file_path("relationship.md")


def update_relationship(note: str) -> None:
    path = relationship_path()
    if not path.exists():
        path.write_text("# Relationship Evolution\n\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"## {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
        handle.write(f"{note.strip()}\n\n")
    print(f"Updated {path}")


def view_relationship() -> None:
    path = relationship_path()
    if not path.exists():
        print("No relationship notes recorded.")
        return
    print(path.read_text(encoding="utf-8").strip())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Agent Chronicle relationship evolution notes.")
    subparsers = parser.add_subparsers(dest="command")

    update_parser = subparsers.add_parser("update", help="Append a relationship evolution note.")
    update_parser.add_argument("note", help="Relationship note.")
    subparsers.add_parser("view", help="View the relationship history.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "update":
        update_relationship(args.note)
    elif args.command == "view":
        view_relationship()
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
