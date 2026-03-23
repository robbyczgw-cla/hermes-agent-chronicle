"""
agent-chronicle — Hermes Plugin v1.0.0
AI-perspective journaling: diary entries, quotes, curiosities, decisions, relationship notes.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).parent / "scripts"


def _run(script: str, args: list) -> dict:
    """Run a chronicle script as subprocess and return result dict."""
    cmd = [sys.executable, str(_SCRIPTS / script)] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout.strip()
        if result.returncode != 0:
            err = result.stderr.strip() or output
            return {"success": False, "error": err}
        return {"success": True, "output": output}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Chronicle script timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── Tool handlers ──────────────────────────────────────────────────────────────

def _chronicle_generate(args: dict, **_) -> str:
    context = args.get("context", "").strip()
    if context:
        import tempfile, os
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
        tmp.write(context)
        tmp.close()
        result = _run("generate.py", ["--from-file", tmp.name])
        try:
            os.unlink(tmp.name)
        except Exception:
            pass
    else:
        result = _run("generate.py", ["--today"])
    return json.dumps(result)


def _chronicle_add_quote(args: dict, **_) -> str:
    quote = args.get("quote", "").strip()
    if not quote:
        return json.dumps({"success": False, "error": "quote is required"})
    script_args = ["add", quote]
    if args.get("context"):
        script_args += ["--context", args["context"]]
    if args.get("source"):
        script_args += ["--source", args["source"]]
    return json.dumps(_run("quotes.py", script_args))


def _chronicle_add_curiosity(args: dict, **_) -> str:
    question = args.get("question", "").strip()
    if not question:
        return json.dumps({"success": False, "error": "question is required"})
    script_args = ["add", question]
    if args.get("priority"):
        script_args += ["--priority", args["priority"]]
    return json.dumps(_run("curiosity.py", script_args))


def _chronicle_add_decision(args: dict, **_) -> str:
    decision = args.get("decision", "").strip()
    reasoning = args.get("reasoning", "").strip()
    if not decision or not reasoning:
        return json.dumps({"success": False, "error": "decision and reasoning are required"})
    script_args = ["add", decision, "--reasoning", reasoning]
    if args.get("outcome"):
        script_args += ["--outcome", args["outcome"]]
    return json.dumps(_run("decisions.py", script_args))


def _chronicle_update_relationship(args: dict, **_) -> str:
    note = args.get("note", "").strip()
    if not note:
        return json.dumps({"success": False, "error": "note is required"})
    return json.dumps(_run("relationship.py", ["update", note]))


def _chronicle_view_today(args: dict, **_) -> str:
    return json.dumps(_run("generate.py", ["--view"]))


def _chronicle_list_quotes(args: dict, **_) -> str:
    return json.dumps(_run("quotes.py", ["list"]))


# ── Plugin registration ────────────────────────────────────────────────────────

def register(ctx: Any) -> None:

    ctx.register_tool(
        name="chronicle_generate",
        toolset="productivity",
        schema={
            "name": "chronicle_generate",
            "description": "Generate today's AI-perspective diary entry and save it to ~/.hermes/chronicle/. Optionally provide session context to make the entry richer.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "Optional summary of today's session or events to include in the diary entry.",
                    }
                },
                "required": [],
            },
        },
        handler=lambda args, **kw: _chronicle_generate(args, **kw),
        emoji="📜",
    )

    ctx.register_tool(
        name="chronicle_add_quote",
        toolset="productivity",
        schema={
            "name": "chronicle_add_quote",
            "description": "Add a memorable quote to the Chronicle Quote Hall of Fame.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "quote": {"type": "string", "description": "The quote text to save."},
                    "context": {"type": "string", "description": "Optional context about when/why this quote matters."},
                    "source": {"type": "string", "description": "Optional source or speaker attribution."},
                },
                "required": ["quote"],
            },
        },
        handler=lambda args, **kw: _chronicle_add_quote(args, **kw),
        emoji="💬",
    )

    ctx.register_tool(
        name="chronicle_add_curiosity",
        toolset="productivity",
        schema={
            "name": "chronicle_add_curiosity",
            "description": "Add a question or topic to the Chronicle Curiosity Backlog — things worth exploring later.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The question or topic to add."},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "Priority level. Default: medium."},
                },
                "required": ["question"],
            },
        },
        handler=lambda args, **kw: _chronicle_add_curiosity(args, **kw),
        emoji="🔮",
    )

    ctx.register_tool(
        name="chronicle_add_decision",
        toolset="productivity",
        schema={
            "name": "chronicle_add_decision",
            "description": "Log a decision to Chronicle Decision Archaeology — records judgment calls with reasoning for later review.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "decision": {"type": "string", "description": "The decision or action taken."},
                    "reasoning": {"type": "string", "description": "Why this decision was made."},
                    "outcome": {"type": "string", "description": "Optional: known outcome or result."},
                },
                "required": ["decision", "reasoning"],
            },
        },
        handler=lambda args, **kw: _chronicle_add_decision(args, **kw),
        emoji="🏛",
    )

    ctx.register_tool(
        name="chronicle_update_relationship",
        toolset="productivity",
        schema={
            "name": "chronicle_update_relationship",
            "description": "Add a note to Chronicle Relationship Evolution — track how the dynamic between agent and user is developing.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "note": {"type": "string", "description": "Note about the relationship dynamic or interaction pattern."},
                },
                "required": ["note"],
            },
        },
        handler=lambda args, **kw: _chronicle_update_relationship(args, **kw),
        emoji="🤝",
    )

    ctx.register_tool(
        name="chronicle_view_today",
        toolset="productivity",
        schema={
            "name": "chronicle_view_today",
            "description": "View today's existing Chronicle diary entry if one has already been generated.",
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        handler=lambda args, **kw: _chronicle_view_today(args, **kw),
        emoji="📖",
    )

    ctx.register_tool(
        name="chronicle_list_quotes",
        toolset="productivity",
        schema={
            "name": "chronicle_list_quotes",
            "description": "List all saved quotes from the Chronicle Quote Hall of Fame.",
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        handler=lambda args, **kw: _chronicle_list_quotes(args, **kw),
        emoji="✨",
    )
