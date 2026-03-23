from __future__ import annotations
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import argparse
from pathlib import Path

from common import (
    VALID_PRIVACY_LEVELS,
    ensure_dir,
    get_chronicle_dir,
    load_config,
    save_config,
)


def prompt_with_default(label: str, default: str) -> str:
    value = input(f"{label} [{default}]: ").strip()
    return value or default


def prompt_yes_no(label: str, default: bool) -> bool:
    suffix = "Y/n" if default else "y/N"
    value = input(f"{label} [{suffix}]: ").strip().lower()
    if not value:
        return default
    return value in {"y", "yes"}


def run_wizard() -> None:
    current = load_config()
    chronicle_dir = get_chronicle_dir()

    privacy = prompt_with_default("Privacy level (private/shareable/public)", current["privacy"])
    while privacy not in VALID_PRIVACY_LEVELS:
        privacy = prompt_with_default("Choose private, shareable, or public", current["privacy"])

    diary_dir_input = prompt_with_default("Diary directory", current["diary_dir"])
    diary_dir = Path(diary_dir_input).expanduser()
    memory_integration = prompt_yes_no(
        "Enable memory integration append to ~/.hermes/memory.md",
        bool(current.get("memory_integration", True)),
    )
    model = prompt_with_default("Hermes model", current["model"])

    ensure_dir(chronicle_dir)
    ensure_dir(diary_dir)

    config = {
        "privacy": privacy,
        "diary_dir": str(diary_dir),
        "memory_integration": memory_integration,
        "model": model,
        "features": {
            "quotes": True,
            "curiosity": True,
            "decisions": True,
            "relationship": True,
            "memory_integration": memory_integration,
        },
    }

    path = save_config(config)
    print(f"Saved configuration to {path}")
    print(f"Diary entries will be stored in {diary_dir}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Interactive setup wizard for Hermes Agent Chronicle."
    )
    return parser


def main() -> None:
    build_parser().parse_args()
    run_wizard()


if __name__ == "__main__":
    main()
