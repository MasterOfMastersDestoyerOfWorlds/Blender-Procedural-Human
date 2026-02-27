"""Decorator-driven CLI for Blender validation and automation."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import traceback
import urllib.error
from pathlib import Path
from typing import Any

# Allow `python tools/blender_cli.py` while preserving package imports.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tools.commands.capture  # noqa: F401
import tools.commands.geometry  # noqa: F401
import tools.commands.lifecycle  # noqa: F401
import tools.commands.node_tools  # noqa: F401
import tools.commands.refactor  # noqa: F401
import tools.commands.validation  # noqa: F401
from tools.cli_registry import CliCommand, get_registry
from tools.commands.common import BlenderClient, DEFAULT_BASE_URL

# Keyword-named module must be imported dynamically.
importlib.import_module("tools.commands.exec")


def _annotation_to_type(annotation: Any) -> Any:
    if annotation in (str, int, float):
        return annotation
    return str


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="blender_cli",
        description="CLI for Blender server lifecycle and geometry validation",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Blender server base URL (default: %(default)s)",
    )
    subparsers = parser.add_subparsers(dest="command_name", required=True)

    for command_name, command in sorted(get_registry().items()):
        _add_command_parser(subparsers, command_name, command)

    return parser


def _add_command_parser(subparsers, command_name: str, command: CliCommand) -> None:
    command_parser = subparsers.add_parser(command_name, help=command.summary, description=command.docstring)
    for parameter in command.params:
        primary_cli_name = f"--{parameter.name.replace('_', '-')}"
        cli_names = [primary_cli_name]
        if parameter.name == "object_name":
            cli_names.append("--object")
        help_text = parameter.help_text

        if parameter.annotation is bool:
            if parameter.has_default and parameter.default is True:
                command_parser.add_argument(
                    f"--no-{parameter.name.replace('_', '-')}",
                    dest=parameter.name,
                    action="store_false",
                    default=True,
                    help=help_text or "Disable this check/feature.",
                )
            else:
                command_parser.add_argument(
                    *cli_names,
                    dest=parameter.name,
                    action="store_true",
                    default=False if parameter.has_default else None,
                    required=not parameter.has_default,
                    help=help_text or "Enable this check/feature.",
                )
            continue

        argument_kwargs: dict[str, Any] = {
            "dest": parameter.name,
            "type": _annotation_to_type(parameter.annotation),
            "help": help_text or None,
        }
        if parameter.has_default:
            argument_kwargs["default"] = parameter.default
        else:
            argument_kwargs["required"] = True
        command_parser.add_argument(*cli_names, **argument_kwargs)


def _run(argv: list[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    registry = get_registry()
    command = registry[args.command_name]

    kwargs = {
        param.name: getattr(args, param.name)
        for param in command.params
    }

    try:
        if command.needs_client:
            client = BlenderClient(base_url=args.base_url)
            result = command.function(client, **kwargs)
        else:
            result = command.function(**kwargs)
    except urllib.error.HTTPError as exc:
        result = {"ok": False, "error": f"HTTP {exc.code}: {exc.reason}"}
    except urllib.error.URLError as exc:
        result = {"ok": False, "error": f"Connection error: {exc.reason}"}
    except Exception as exc:
        result = {
            "ok": False,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }

    print(json.dumps(result, indent=2))
    return 0 if result.get("ok", False) else 2


def main() -> int:
    """Entry point wrapper."""
    return _run(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
