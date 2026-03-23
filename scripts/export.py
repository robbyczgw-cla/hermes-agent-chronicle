from __future__ import annotations
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import argparse
import shutil
import subprocess
import tempfile
from datetime import date, timedelta
from pathlib import Path
from typing import List

from common import format_date, get_diary_dir, load_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export recent Hermes chronicle entries.")
    parser.add_argument(
        "--format",
        choices=("pdf", "html", "markdown"),
        default="markdown",
        help="Export format.",
    )
    parser.add_argument("--days", type=int, default=7, help="Number of days to include.")
    parser.add_argument("--output", required=True, help="Output file path.")
    return parser


def collect_entries(days: int) -> List[Path]:
    config = load_config()
    diary_dir = get_diary_dir(config)
    today = date.today()
    paths: List[Path] = []
    for offset in range(days):
        candidate = diary_dir / f"{format_date(today - timedelta(days=offset))}.md"
        if candidate.exists():
            paths.append(candidate)
    return sorted(paths)


def build_markdown(entries: List[Path]) -> str:
    parts: List[str] = ["# Agent Chronicle Export"]
    for entry in entries:
        parts.append(entry.read_text(encoding="utf-8").strip())
    return "\n\n".join(part for part in parts if part).rstrip() + "\n"


def export_markdown(output_path: Path, content: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote markdown export to {output_path}")


def export_via_pandoc(output_path: Path, content: str, fmt: str) -> None:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        print("Pandoc is not installed. Install pandoc to export PDF or HTML.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as handle:
        handle.write(content)
        temp_path = Path(handle.name)

    try:
        cmd = [pandoc, "--sandbox", str(temp_path), "-o", str(output_path)]
        if fmt == "html":
            cmd.extend(["--standalone", "--to", "html5"])
        subprocess.run(cmd, check=True)
        print(f"Wrote {fmt} export to {output_path}")
    except subprocess.CalledProcessError as exc:
        print(f"Pandoc export failed: {exc}")
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> None:
    args = build_parser().parse_args()
    entries = collect_entries(args.days)
    if not entries:
        print("No entries found for the requested date range.")
        return

    content = build_markdown(entries)
    output_path = Path(args.output).expanduser()
    if args.format == "markdown":
        export_markdown(output_path, content)
        return
    export_via_pandoc(output_path, content, args.format)


if __name__ == "__main__":
    main()
