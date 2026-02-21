"""Decorator-driven command registry for Blender CLI."""

from __future__ import annotations

import inspect
import re
from dataclasses import dataclass
from typing import Any, Callable, get_args, get_origin


@dataclass(frozen=True)
class CliParameter:
    """Parsed metadata for a single CLI command parameter."""

    name: str
    annotation: Any
    has_default: bool
    default: Any
    help_text: str


@dataclass(frozen=True)
class CliCommand:
    """Metadata for a decorated CLI command."""

    name: str
    function: Callable[..., dict]
    summary: str
    docstring: str
    params: list[CliParameter]


_REGISTRY: dict[str, CliCommand] = {}
_PARAM_RE = re.compile(r"^\s*:param\s+(\w+)\s*:\s*(.+)\s*$")


def _normalize_annotation(annotation: Any) -> Any:
    """Normalize Optional/Union annotations to a concrete parser type."""
    if annotation is inspect._empty:
        return str

    origin = get_origin(annotation)
    if origin is None:
        return annotation

    args = [arg for arg in get_args(annotation) if arg is not type(None)]
    if len(args) == 1:
        return args[0]
    return str


def _parse_docstring(function: Callable[..., dict]) -> tuple[str, str, dict[str, str]]:
    """Extract a summary and :param docs from a command docstring."""
    doc = inspect.getdoc(function) or ""
    if not doc.strip():
        raise ValueError(
            f"CLI command '{function.__name__}' is missing a docstring. "
            "Add a summary and :param docs."
        )

    lines = doc.splitlines()
    summary = lines[0].strip()
    if not summary:
        raise ValueError(f"CLI command '{function.__name__}' has an empty docstring summary.")

    param_help: dict[str, str] = {}
    for line in lines:
        match = _PARAM_RE.match(line)
        if match:
            param_help[match.group(1)] = match.group(2).strip()

    return summary, doc, param_help


def cli_command(function: Callable[..., dict]) -> Callable[..., dict]:
    """Register a function as a CLI command."""
    summary, docstring, param_help = _parse_docstring(function)
    signature = inspect.signature(function)
    params: list[CliParameter] = []

    for index, parameter in enumerate(signature.parameters.values()):
        if index == 0 and parameter.name == "client":
            continue

        annotation = _normalize_annotation(parameter.annotation)
        has_default = parameter.default is not inspect._empty
        default = parameter.default if has_default else None
        help_text = param_help.get(parameter.name, "")
        if not help_text:
            raise ValueError(
                f"CLI command '{function.__name__}' is missing ':param {parameter.name}:' documentation."
            )
        params.append(
            CliParameter(
                name=parameter.name,
                annotation=annotation,
                has_default=has_default,
                default=default,
                help_text=help_text,
            )
        )

    command_name = function.__name__.replace("_", "-")
    if command_name in _REGISTRY:
        raise ValueError(f"CLI command '{command_name}' is already registered.")

    _REGISTRY[command_name] = CliCommand(
        name=command_name,
        function=function,
        summary=summary,
        docstring=docstring,
        params=params,
    )
    return function


def get_registry() -> dict[str, CliCommand]:
    """Return all registered CLI commands."""
    return _REGISTRY.copy()
