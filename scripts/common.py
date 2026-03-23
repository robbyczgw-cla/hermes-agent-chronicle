from __future__ import annotations

import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Optional

import requests


DEFAULT_MODEL = "anthropic/claude-sonnet-4-6"
DEFAULT_PRIVACY = "private"
VALID_PRIVACY_LEVELS = {"private", "shareable", "public"}
CONFIG_FILENAME = "config.json"
MEMORY_FILENAME = "memory.md"


def expand_path(value: str) -> Path:
    return Path(value).expanduser()


def get_chronicle_dir() -> Path:
    override = os.getenv("HERMES_CHRONICLE_DIR")
    if override:
        return expand_path(override)
    return Path.home() / ".hermes" / "chronicle"


def get_config_path() -> Path:
    return get_chronicle_dir() / CONFIG_FILENAME


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_config() -> Dict[str, Any]:
    chronicle_dir = get_chronicle_dir()
    return {
        "privacy": DEFAULT_PRIVACY,
        "diary_dir": str(chronicle_dir),
        "memory_integration": True,
        "model": os.getenv("HERMES_CHRONICLE_MODEL", DEFAULT_MODEL),
        "features": {
            "quotes": True,
            "curiosity": True,
            "decisions": True,
            "relationship": True,
            "memory_integration": True,
        },
    }


def load_config() -> Dict[str, Any]:
    path = get_config_path()
    if not path.exists():
        return default_config()

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    merged = default_config()
    merged.update(data)
    merged["features"] = {
        **default_config()["features"],
        **data.get("features", {}),
    }
    merged["diary_dir"] = str(
        expand_path(merged.get("diary_dir", str(get_chronicle_dir())))
    )
    return merged


def save_config(config: Dict[str, Any]) -> Path:
    chronicle_dir = ensure_dir(get_chronicle_dir())
    path = chronicle_dir / CONFIG_FILENAME
    payload = default_config()
    payload.update(config)
    payload["diary_dir"] = str(expand_path(payload["diary_dir"]))
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return path


def get_diary_dir(config: Optional[Dict[str, Any]] = None) -> Path:
    config = config or load_config()
    return ensure_dir(expand_path(config.get("diary_dir", str(get_chronicle_dir()))))


def get_entry_path(entry_date: date, config: Optional[Dict[str, Any]] = None) -> Path:
    return get_diary_dir(config) / f"{entry_date.isoformat()}.md"


def get_support_file_path(filename: str) -> Path:
    return ensure_dir(get_chronicle_dir()) / filename


def append_memory_integration(summary: str) -> Path:
    memory_path = Path.home() / ".hermes" / MEMORY_FILENAME
    ensure_dir(memory_path.parent)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with memory_path.open("a", encoding="utf-8") as handle:
        handle.write(f"- {timestamp}: {summary.strip()}\n")
    return memory_path


def format_date(entry_date: date) -> str:
    return entry_date.strftime("%Y-%m-%d")


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def read_template(name: str) -> str:
    template_path = Path(__file__).resolve().parent.parent / "templates" / name
    with template_path.open("r", encoding="utf-8") as handle:
        return handle.read()


def render_template(name: str, context: Dict[str, str]) -> str:
    rendered = read_template(name)
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def call_hermes_api(prompt: str, system: str, model: str) -> str:
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("HERMES_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model or os.getenv("HERMES_CHRONICLE_MODEL", DEFAULT_MODEL),
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.8,
    }

    response = requests.post(
        "http://localhost:8642/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Hermes API returned an unexpected response shape.") from exc
