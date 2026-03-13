"""Lifecycle commands for Blender process management."""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
from pathlib import Path

from tools.cli_registry import cli_command
from tools.commands.common import (
    BlenderClient,
    clear_session,
    get_session_path,
    read_session,
    write_session,
)

TOOLS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = TOOLS_DIR.parent
PID_PATH = REPO_ROOT / "tmp" / ".blender_pid"
CONFIG_PATH = TOOLS_DIR / "blender_config.json"
BOOTSTRAP_PATH = TOOLS_DIR / "blender_bootstrap.py"
BLENDER_LOG_PATH = REPO_ROOT / "tmp" / "blender-server.log"


def _find_free_port() -> int:
    """Return a free port for the Blender server to bind to."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def _resolve_blender_executable(explicit_path: str = "") -> tuple[str | None, str | None]:
    if explicit_path:
        return explicit_path, None
    env_path = os.getenv("BLENDER_EXE", "").strip()
    if env_path:
        return env_path, None
    if CONFIG_PATH.exists():
        try:
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            config_path = str(config.get("blender_executable", "")).strip()
            if config_path:
                return config_path, None
        except json.JSONDecodeError as exc:
            return None, f"Invalid JSON in {CONFIG_PATH}: {exc}"

    vscode_settings_path = REPO_ROOT / ".vscode" / "settings.json"
    if vscode_settings_path.exists():
        try:
            settings = json.loads(vscode_settings_path.read_text(encoding="utf-8"))
            executables = settings.get("blender.executables", [])
            if isinstance(executables, list):
                default_path = ""
                for item in executables:
                    if not isinstance(item, dict):
                        continue
                    path_value = str(item.get("path", "")).strip()
                    if not path_value:
                        continue
                    if item.get("isDefault", False):
                        default_path = path_value
                        break
                    if not default_path:
                        default_path = path_value
                if default_path:
                    return default_path, None
        except json.JSONDecodeError:
            pass

    which_path = shutil.which("blender")
    if which_path:
        return which_path, None

    return None, (
        "No Blender executable configured. Use --blender, BLENDER_EXE env var, "
        "tools/blender_config.json, .vscode blender.executables, or ensure 'blender' is on PATH."
    )


def _write_pid(pid: int) -> None:
    PID_PATH.parent.mkdir(parents=True, exist_ok=True)
    PID_PATH.write_text(str(pid), encoding="utf-8")


def _clear_pid() -> None:
    if PID_PATH.exists():
        PID_PATH.unlink()


def _read_pid() -> int | None:
    """Legacy: read PID from global file (for backward compat with pre-session runs)."""
    if not PID_PATH.exists():
        return None
    try:
        return int(PID_PATH.read_text(encoding="utf-8").strip())
    except (TypeError, ValueError):
        return None


def _kill_pid(pid: int) -> tuple[bool, str]:
    if os.name == "nt":
        result = subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return True, "Blender process terminated."
        return False, (result.stderr or result.stdout or "taskkill failed").strip()
    try:
        os.kill(pid, 15)
        return True, "Blender process terminated."
    except OSError as exc:
        return False, str(exc)


@cli_command
def ping(client: BlenderClient) -> dict:
    """Check if Blender server is alive.

    :param client: Blender HTTP client.
    """
    if client.ping_with_backoff(max_attempts=1):
        return {"ok": True, "message": "Blender server is running"}
    return {"ok": False, "error": "Unable to reach Blender server"}


@cli_command
def start(
    client: BlenderClient,
    blender: str = "",
    blend_file: str = "",
    headless: bool = True,
) -> dict:
    """Start Blender in background and wait for server health.

    Uses a free port and writes .blender-session.json in the current directory
    so subsequent commands (ping, validate, shutdown) find this instance.
    Headless (-b) by default so no GUI is shown and stdout/stderr go to a log file.

    :param client: Blender HTTP client (base_url ignored; port comes from new session).
    :param blender: Optional path to Blender executable.
    :param blend_file: Optional blend file to open on startup.
    :param headless: If True (default), run with -b and redirect output to log.
    """
    session = read_session()
    if session and isinstance(session.get("port"), int):
        check_client = BlenderClient(base_url=f"http://localhost:{session['port']}")
        if check_client.ping_with_backoff(max_attempts=1):
            return {
                "ok": True,
                "pid": session.get("pid"),
                "port": session["port"],
                "message": "Blender already running for this directory.",
            }

    blender_executable, error = _resolve_blender_executable(blender)
    if error:
        return {"ok": False, "error": error}

    port = _find_free_port()
    env = os.environ.copy()
    env["BLENDER_SERVER_PORT"] = str(port)

    command: list[str] = [blender_executable]
    if headless:
        command.append("-b")
    if blend_file:
        command.append(blend_file)
    command.extend(["--python", str(BOOTSTRAP_PATH)])

    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    BLENDER_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log_file = open(BLENDER_LOG_PATH, "w", encoding="utf-8")

    process = subprocess.Popen(
        command,
        cwd=str(REPO_ROOT),
        stdout=log_file,
        stderr=subprocess.STDOUT,
        env=env,
        creationflags=creationflags,
    )
    log_file.close()

    write_session(port=port, pid=process.pid, backend="process")

    session_client = BlenderClient(base_url=f"http://localhost:{port}")
    healthy = session_client.ping_with_backoff(max_attempts=10, base_delay=0.5)
    if not healthy:
        return {
            "ok": False,
            "pid": process.pid,
            "port": port,
            "error": "Blender launched but server did not become healthy in time.",
        }
    return {
        "ok": True,
        "pid": process.pid,
        "port": port,
        "message": "Blender started and server is healthy.",
    }


@cli_command
def reload(client: BlenderClient, keep_scene: bool = False) -> dict:
    """Reload addon, optionally resetting to a clean scene first.

    :param client: Blender HTTP client.
    :param keep_scene: Keep current scene if true. Default reload resets scene.
    """
    result = client.command("reload_addon", {"clean_scene": not keep_scene})
    result["ok"] = bool(result.get("success"))
    return result


def _stop_container(container_id: str) -> tuple[bool, str]:
    """Stop and remove a Docker container. Returns (success, message)."""
    try:
        r = subprocess.run(
            ["docker", "stop", container_id],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if r.returncode == 0:
            return True, "Container stopped."
        return False, (r.stderr or r.stdout or "docker stop failed").strip()
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return False, str(e)


@cli_command
def shutdown(client: BlenderClient) -> dict:
    """Shutdown Blender for this directory (session file or legacy PID), or via server quit.

    :param client: Blender HTTP client (used when no session/PID found).
    """
    session = read_session()
    if session:
        backend = session.get("backend", "process")
        if backend == "container" and session.get("container_id"):
            cid = session["container_id"]
            ok, msg = _stop_container(cid)
            clear_session()
            if ok:
                return {"ok": True, "method": "container", "container_id": cid, "message": msg}
            return {"ok": False, "method": "container", "container_id": cid, "error": msg}
        pid = session.get("pid")
        if isinstance(pid, int):
            ok, message = _kill_pid(pid)
            clear_session()
            if ok:
                return {"ok": True, "method": "session", "pid": pid, "message": message}
            return {"ok": False, "method": "session", "pid": pid, "error": message}

    pid = _read_pid()
    if pid is not None:
        ok, message = _kill_pid(pid)
        if ok:
            _clear_pid()
            clear_session()
            return {"ok": True, "method": "pid", "pid": pid, "message": message}
        return {"ok": False, "method": "pid", "pid": pid, "error": message}

    try:
        result = client.command("exec_python", {"code": "import bpy; bpy.ops.wm.quit_blender()"})
        if result.get("success"):
            clear_session()
            return {
                "ok": True,
                "method": "server",
                "message": "Sent wm.quit_blender via Blender server.",
            }
        return {
            "ok": False,
            "method": "server",
            "error": "No tracked PID and server quit command failed.",
            "details": result,
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": (
                "No session or PID for this directory and unable to reach Blender server. "
                f"{exc}"
            ),
        }


@cli_command
def restart(client: BlenderClient, blender: str = "", blend_file: str = "") -> dict:
    """Restart Blender by killing tracked PID and starting again.

    :param client: Blender HTTP client.
    :param blender: Optional path to Blender executable.
    :param blend_file: Optional blend file to open on startup.
    """
    killed = shutdown(client)

    started = start(client, blender=blender, blend_file=blend_file)
    if not started.get("ok"):
        return {"ok": False, "killed": killed, "start": started}
    return {"ok": True, "killed": killed, "start": started}
