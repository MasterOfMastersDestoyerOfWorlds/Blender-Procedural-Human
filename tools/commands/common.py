"""Shared helpers for Blender CLI commands."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_BASE_URL = "http://localhost:9876"
COMMAND_TIMEOUT_SECONDS = 30


@dataclass
class BlenderClient:
    """Small HTTP client for the Blender in-process test server."""

    base_url: str = DEFAULT_BASE_URL

    def _request(self, path: str, body: dict[str, Any] | None = None, timeout: int = 60) -> dict[str, Any]:
        payload = None
        method = "GET"
        headers = {"Content-Type": "application/json"}
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            method = "POST"
        req = urllib.request.Request(
            self.base_url.rstrip("/") + path,
            data=payload,
            headers=headers,
            method=method,
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def command(self, action: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Call `/command` on Blender server."""
        return self._request(
            "/command",
            {"action": action, "params": params or {}},
            timeout=COMMAND_TIMEOUT_SECONDS,
        )

    def health(self) -> dict[str, Any]:
        """Call `/health` on Blender server."""
        return self._request("/health", None, timeout=10)

    def ping_with_backoff(self, max_attempts: int = 8, base_delay: float = 0.5) -> bool:
        """Poll health endpoint with exponential backoff."""
        for attempt in range(max_attempts):
            try:
                result = self.health()
                if result.get("healthy"):
                    return True
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
                pass
            time.sleep(base_delay * (2 ** attempt))
        return False


def parse_inputs(inputs: str) -> tuple[dict[str, Any], str | None]:
    """Parse JSON string inputs payload for apply/validate commands."""
    if not inputs:
        return {}, None
    try:
        parsed = json.loads(inputs)
    except json.JSONDecodeError as exc:
        return {}, f"Invalid JSON for --inputs: {exc}"
    if not isinstance(parsed, dict):
        return {}, "Invalid JSON for --inputs: expected an object."
    return parsed, None
