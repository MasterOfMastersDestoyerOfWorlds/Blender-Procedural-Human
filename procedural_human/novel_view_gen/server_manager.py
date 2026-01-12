"""
Hunyuan3D API Server Manager

Manages the Hunyuan3D API server as a subprocess. The server is started
when the Blender addon loads and stopped when Blender quits (not on addon reload).

Usage:
    from procedural_human.novel_view_gen.server_manager import (
        start_hunyuan_server,
        stop_hunyuan_server,
        is_server_running,
    )
    
    # Start server (called during addon register)
    start_hunyuan_server()
    
    # Check if running
    if is_server_running():
        print("Server is up!")
    
    # Stop server (called via atexit on Blender quit)
    stop_hunyuan_server()
"""

import subprocess
import threading
import time
import os
import sys
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error

from procedural_human.logger import logger

# Server state
_server_process: Optional[subprocess.Popen] = None
_server_thread: Optional[threading.Thread] = None
_server_port: int = 8082
_server_host: str = "localhost"

# Default paths - can be configured via preferences
_hunyuan_install_path: Optional[str] = None
_python_executable: Optional[str] = None


def _is_valid_hunyuan_install(path: Path) -> bool:
    """Check if a path contains a valid Hunyuan3D installation with api_server.py."""
    return path.exists() and (path / "api_server.py").exists()


def _get_addon_root() -> Path:
    """Get the root directory of the procedural_human addon."""
    # This file is at: procedural_human/novel_view_gen/server_manager.py
    # Addon root is: procedural_human/
    return Path(__file__).parent.parent


def _get_submodule_path() -> Path:
    """Get the path to the Hunyuan3D-2 submodule (procedural_human/novel_view_gen/Hunyuan3D-2)."""
    # Submodule is at: procedural_human/novel_view_gen/Hunyuan3D-2
    # This file is at: procedural_human/novel_view_gen/server_manager.py
    return Path(__file__).parent / "Hunyuan3D-2"


def _get_novel_view_gen_path() -> Path:
    """Get the path to the novel_view_gen directory."""
    return Path(__file__).parent


def get_local_model_weights_path() -> Optional[Path]:
    """
    Check for local model weights in the novel_view_gen directory.
    
    The Hunyuan3D loader expects files in:
    {HY3DGEN_MODELS}/{model_path}/{subfolder}/
    
    For the mini turbo model:
    {HY3DGEN_MODELS}/tencent/Hunyuan3D-2mini/hunyuan3d-dit-v2-mini-turbo/
        ├── config.yaml
        └── model.fp16.safetensors
    
    For the VAE model:
    {HY3DGEN_MODELS}/tencent/Hunyuan3D-2mini/hunyuan3d-vae-v2-mini-turbo/
        ├── config.yaml
        └── model.fp16.safetensors
    
    Files can be placed in:
    - novel_view_gen/ directly
    - novel_view_gen/weights/ directory
    
    Returns:
        Path to the base directory for HY3DGEN_MODELS, or None if no local weights.
    """
    novel_view_gen = _get_novel_view_gen_path()
    weights_base = novel_view_gen / "weights"
    
    # Check multiple possible source locations for model files
    # Priority: weights/ directory, then novel_view_gen/ directly
    source_dirs = [weights_base, novel_view_gen]
    
    source_dir = None
    safetensors_file = None
    ckpt_file = None
    config_file = None
    vae_config_file = None
    
    for src in source_dirs:
        sf = src / "model.fp16.safetensors"
        ck = src / "model.fp16.ckpt"
        cf = src / "config.yaml"
        vf = src / "vae.config.yaml"
        
        has_weights = sf.exists() or ck.exists()
        has_config = cf.exists()
        
        if has_weights and has_config:
            source_dir = src
            safetensors_file = sf if sf.exists() else None
            ckpt_file = ck if ck.exists() else None
            config_file = cf
            vae_config_file = vf if vf.exists() else None
            break
    
    if source_dir is not None:
        # Local weights found - set up the correct path structure
        # DiT model: hunyuan3d-dit-v2-mini-turbo
        # VAE model: hunyuan3d-vae-v2-mini-turbo
        
        dit_dir = weights_base / "tencent" / "Hunyuan3D-2mini" / "hunyuan3d-dit-v2-mini-turbo"
        vae_dir = weights_base / "tencent" / "Hunyuan3D-2mini" / "hunyuan3d-vae-v2-mini-turbo"
        
        import shutil
        
        # Set up DiT model directory
        if not dit_dir.exists() or not (dit_dir / "config.yaml").exists():
            try:
                dit_dir.mkdir(parents=True, exist_ok=True)
                
                if config_file and config_file.exists() and not (dit_dir / "config.yaml").exists():
                    shutil.copy2(config_file, dit_dir / "config.yaml")
                    logger.info(f"[Hunyuan3D] Copied config.yaml to {dit_dir}")
                
                if safetensors_file and safetensors_file.exists() and not (dit_dir / "model.fp16.safetensors").exists():
                    shutil.copy2(safetensors_file, dit_dir / "model.fp16.safetensors")
                    logger.info(f"[Hunyuan3D] Copied model.fp16.safetensors to {dit_dir}")
                
                if ckpt_file and ckpt_file.exists() and not (dit_dir / "model.fp16.ckpt").exists():
                    shutil.copy2(ckpt_file, dit_dir / "model.fp16.ckpt")
                    logger.info(f"[Hunyuan3D] Copied model.fp16.ckpt to {dit_dir}")
                    
            except Exception as e:
                logger.warning(f"[Hunyuan3D] Failed to set up DiT model directory: {e}")
                return None
        
        # Set up VAE model directory if we have vae config
        if vae_config_file and vae_config_file.exists() and not (vae_dir / "config.yaml").exists():
            try:
                vae_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(vae_config_file, vae_dir / "config.yaml")
                logger.info(f"[Hunyuan3D] Copied vae.config.yaml to {vae_dir}/config.yaml")
                
                # Check for separate VAE weights in source directory
                vae_safetensors = source_dir / "vae.model.fp16.safetensors"
                vae_ckpt = source_dir / "vae.model.fp16.ckpt"
                
                if vae_safetensors.exists() and not (vae_dir / "model.fp16.safetensors").exists():
                    shutil.copy2(vae_safetensors, vae_dir / "model.fp16.safetensors")
                    logger.info(f"[Hunyuan3D] Copied vae.model.fp16.safetensors to {vae_dir}")
                elif vae_ckpt.exists() and not (vae_dir / "model.fp16.ckpt").exists():
                    shutil.copy2(vae_ckpt, vae_dir / "model.fp16.ckpt")
                    logger.info(f"[Hunyuan3D] Copied vae.model.fp16.ckpt to {vae_dir}")
                    
            except Exception as e:
                logger.warning(f"[Hunyuan3D] Failed to set up VAE model directory: {e}")
                # Continue - VAE might be downloaded from HuggingFace
        
        return weights_base
    
    # Check if weights are already in the expected structure
    expected_dit_dir = weights_base / "tencent" / "Hunyuan3D-2mini" / "hunyuan3d-dit-v2-mini-turbo"
    expected_safetensors = expected_dit_dir / "model.fp16.safetensors"
    expected_ckpt = expected_dit_dir / "model.fp16.ckpt"
    expected_config = expected_dit_dir / "config.yaml"
    
    if expected_config.exists() and (expected_safetensors.exists() or expected_ckpt.exists()):
        return weights_base
    
    return None


def get_hunyuan_path() -> Optional[Path]:
    """
    Get the path to the Hunyuan3D-2 installation.
    
    Checks in order:
    1. Configured path in addon preferences (must have api_server.py)
    2. Environment variable HUNYUAN3D_PATH (must have api_server.py)
    3. Git submodule at procedural_human/novel_view_gen/Hunyuan3D-2
    4. Common installation locations
    
    Returns:
        Path to Hunyuan3D-2 directory or None if not found
    """
    global _hunyuan_install_path
    
    # Check configured path (must have api_server.py)
    if _hunyuan_install_path:
        configured = Path(_hunyuan_install_path)
        if _is_valid_hunyuan_install(configured):
            return configured
    
    # Check environment variable (must have api_server.py)
    env_path = os.environ.get("HUNYUAN3D_PATH")
    if env_path:
        env_dir = Path(env_path)
        if _is_valid_hunyuan_install(env_dir):
            return env_dir
    
    # Check git submodule location (tools/Hunyuan3D-2)
    submodule_path = _get_submodule_path()
    if _is_valid_hunyuan_install(submodule_path):
        return submodule_path
    
    # Check common locations
    common_paths = [
        Path.home() / "Hunyuan3D-2",
        Path.home() / "hunyuan3d-2",
        Path("C:/Hunyuan3D-2"),
        Path("C:/Users") / os.environ.get("USERNAME", "") / "Hunyuan3D-2",
    ]
    
    for path in common_paths:
        if _is_valid_hunyuan_install(path):
            return path
    
    return None


def get_python_executable() -> str:
    """
    Get the Python executable for running the Hunyuan3D server.
    
    Returns:
        Path to Python executable (uses configured path or system Python)
    """
    global _python_executable
    
    if _python_executable and Path(_python_executable).exists():
        return _python_executable
    
    # Check for venv in Hunyuan3D directory
    hunyuan_path = get_hunyuan_path()
    if hunyuan_path:
        venv_python = hunyuan_path / ".venv" / "Scripts" / "python.exe"
        if venv_python.exists():
            return str(venv_python)
        
        # Check for conda env
        conda_python = hunyuan_path / "venv" / "Scripts" / "python.exe"
        if conda_python.exists():
            return str(conda_python)
    
    # Fall back to system Python
    return sys.executable


def configure_server(
    install_path: Optional[str] = None,
    python_path: Optional[str] = None,
    host: str = "localhost",
    port: int = 8082
):
    """
    Configure the Hunyuan3D server settings.
    
    Args:
        install_path: Path to Hunyuan3D-2 installation directory
        python_path: Path to Python executable for running the server
        host: Host to bind the server to
        port: Port to run the server on
    """
    global _hunyuan_install_path, _python_executable, _server_host, _server_port
    
    if install_path:
        _hunyuan_install_path = install_path
    if python_path:
        _python_executable = python_path
    _server_host = host
    _server_port = port


# Server startup status for async tracking
_server_starting: bool = False
_server_start_error: Optional[str] = None


def is_server_starting() -> bool:
    """Check if server is currently starting up."""
    return _server_starting


def get_server_start_error() -> Optional[str]:
    """Get the last server start error, if any."""
    return _server_start_error


def start_hunyuan_server(
    port: Optional[int] = None,
    host: Optional[str] = None,
    model_path: str = "tencent/Hunyuan3D-2mini",
    device: str = "cuda",
    enable_tex: bool = False,
    blocking: bool = False,
) -> bool:
    """
    Start the Hunyuan3D API server as a subprocess.
    
    Args:
        port: Port to run on (default: 8082)
        host: Host to bind to (default: localhost)
        model_path: HuggingFace model path
        device: Device to run on (cuda or cpu)
        enable_tex: Enable texture generation (requires more VRAM)
        blocking: If True, wait for server to be ready. If False, start in background.
        
    Returns:
        True if server started (or starting if non-blocking), False on error
    """
    global _server_process, _server_port, _server_host, _server_starting, _server_start_error
    
    if _server_process is not None:
        logger.info("[Hunyuan3D] Server already running")
        return True
    
    if _server_starting:
        logger.info("[Hunyuan3D] Server already starting...")
        return True
    
    hunyuan_path = get_hunyuan_path()
    if hunyuan_path is None:
        _server_start_error = "Hunyuan3D-2 installation not found"
        logger.warning(f"[Hunyuan3D] {_server_start_error}. "
                      "Set HUNYUAN3D_PATH environment variable or run setup_hunyuan3d.ps1")
        return False
    
    api_server_script = hunyuan_path / "api_server.py"
    if not api_server_script.exists():
        _server_start_error = f"api_server.py not found at {api_server_script}"
        logger.error(f"[Hunyuan3D] {_server_start_error}")
        return False
    
    if port:
        _server_port = port
    if host:
        _server_host = host
    
    python_exe = get_python_executable()
    
    # Check for local model weights
    local_weights_path = get_local_model_weights_path()
    env = os.environ.copy()
    
    if local_weights_path:
        env["HY3DGEN_MODELS"] = str(local_weights_path)
        logger.info(f"[Hunyuan3D] Using local model weights from: {local_weights_path}")
    
    # Build command with valid api_server.py arguments only
    cmd = [
        python_exe,
        str(api_server_script),
        "--host", _server_host,
        "--port", str(_server_port),
        "--model_path", model_path,
        "--device", device,
    ]
    
    if enable_tex:
        cmd.append("--enable_tex")
    
    logger.info(f"[Hunyuan3D] Starting server: {' '.join(cmd)}")
    
    if blocking:
        return _start_server_blocking(cmd, hunyuan_path, env)
    else:
        # Start in background thread
        _server_starting = True
        _server_start_error = None
        thread = threading.Thread(
            target=_start_server_async,
            args=(cmd, hunyuan_path, env),
            daemon=True
        )
        thread.start()
        return True


def _start_server_blocking(cmd: list, cwd: Path, env: dict = None) -> bool:
    """Start server and wait for it to be ready (blocking)."""
    global _server_process, _server_starting, _server_start_error
    
    try:
        _server_process = subprocess.Popen(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        
        # Start thread to log output
        _start_output_logger()
        
        # Wait for server to be ready
        ready = _wait_for_server_ready(timeout=120)
        
        if ready:
            logger.info(f"[Hunyuan3D] Server started on http://{_server_host}:{_server_port}")
            return True
        else:
            _server_start_error = "Server failed to start within timeout"
            logger.error(f"[Hunyuan3D] {_server_start_error}")
            stop_hunyuan_server()
            return False
            
    except Exception as e:
        _server_start_error = str(e)
        logger.error(f"[Hunyuan3D] Failed to start server: {e}")
        _server_process = None
        return False


def _start_server_async(cmd: list, cwd: Path, env: dict = None):
    """Start server in background thread (non-blocking)."""
    global _server_process, _server_starting, _server_start_error
    
    try:
        logger.info(f"[Hunyuan3D] Spawning subprocess with cwd={cwd}")
        if env and "HY3DGEN_MODELS" in env:
            logger.info(f"[Hunyuan3D] HY3DGEN_MODELS={env['HY3DGEN_MODELS']}")
        
        _server_process = subprocess.Popen(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        
        logger.info(f"[Hunyuan3D] Process started with PID {_server_process.pid}")
        
        # Give the process a moment to start
        time.sleep(1)
        
        # Check if process immediately crashed
        poll_result = _server_process.poll()
        if poll_result is not None:
            stderr_output = ""
            try:
                stderr_output = _server_process.stderr.read()
            except:
                pass
            _server_start_error = f"Process exited immediately with code {poll_result}"
            if stderr_output:
                _server_start_error += f": {stderr_output[:1000]}"
            logger.error(f"[Hunyuan3D] {_server_start_error}")
            _server_process = None
            return
        
        # Start thread to log output
        _start_output_logger()
        
        # Wait for server to be ready (up to 120 seconds)
        ready = _wait_for_server_ready(timeout=120)
        
        if ready:
            logger.info(f"[Hunyuan3D] Server started on http://{_server_host}:{_server_port}")
        else:
            # Check if process died
            if _server_process and _server_process.poll() is not None:
                exit_code = _server_process.returncode
                # Try to get stderr
                stderr_output = ""
                if _server_process.stderr:
                    try:
                        stderr_output = _server_process.stderr.read()
                    except:
                        pass
                _server_start_error = f"Server exited with code {exit_code}"
                if stderr_output:
                    _server_start_error += f": {stderr_output[:500]}"
                logger.error(f"[Hunyuan3D] {_server_start_error}")
            else:
                _server_start_error = "Server did not respond within timeout"
                logger.error(f"[Hunyuan3D] {_server_start_error}")
            stop_hunyuan_server()
            
    except Exception as e:
        _server_start_error = str(e)
        logger.error(f"[Hunyuan3D] Failed to start server: {e}")
        _server_process = None
    finally:
        _server_starting = False


def _start_output_logger():
    """Start threads to log server stdout and stderr."""
    global _server_thread
    
    def log_stdout():
        if _server_process and _server_process.stdout:
            try:
                for line in _server_process.stdout:
                    # Log at INFO level so user can see startup messages
                    logger.info(f"[Hunyuan3D Server] {line.rstrip()}")
            except Exception as e:
                logger.warning(f"[Hunyuan3D] stdout logger error: {e}")
    
    def log_stderr():
        if _server_process and _server_process.stderr:
            try:
                for line in _server_process.stderr:
                    # Log stderr as warnings/errors
                    logger.warning(f"[Hunyuan3D Server ERR] {line.rstrip()}")
            except Exception as e:
                logger.warning(f"[Hunyuan3D] stderr logger error: {e}")
    
    _server_thread = threading.Thread(target=log_stdout, daemon=True)
    _server_thread.start()
    
    stderr_thread = threading.Thread(target=log_stderr, daemon=True)
    stderr_thread.start()


def _wait_for_server_ready(timeout: float = 120, poll_interval: float = 2.0) -> bool:
    """
    Wait for the server to respond to health checks.
    
    Args:
        timeout: Maximum time to wait in seconds
        poll_interval: Time between health check attempts
        
    Returns:
        True if server is ready, False if timeout reached
    """
    start_time = time.time()
    check_count = 0
    
    while time.time() - start_time < timeout:
        check_count += 1
        elapsed = int(time.time() - start_time)
        
        if is_server_running():
            logger.info(f"[Hunyuan3D] Server responded after {elapsed}s")
            return True
        
        # Check if process died
        if _server_process and _server_process.poll() is not None:
            logger.error(f"[Hunyuan3D] Server process exited with code {_server_process.returncode}")
            return False
        
        # Log progress every 10 seconds
        if check_count % 5 == 0:
            logger.info(f"[Hunyuan3D] Waiting for server... ({elapsed}s elapsed, PID {_server_process.pid if _server_process else 'None'})")
        
        time.sleep(poll_interval)
    
    return False


def stop_hunyuan_server():
    """
    Stop the Hunyuan3D API server.
    
    This is called via atexit when Blender quits (not on addon reload).
    """
    global _server_process, _server_thread
    
    if _server_process is None:
        return
    
    logger.info("[Hunyuan3D] Stopping server...")
    
    try:
        # Try graceful shutdown first
        _server_process.terminate()
        
        # Wait for process to exit (with timeout)
        try:
            _server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if graceful shutdown fails
            logger.warning("[Hunyuan3D] Server did not stop gracefully, forcing kill")
            _server_process.kill()
            _server_process.wait(timeout=2)
        
        logger.info("[Hunyuan3D] Server stopped")
        
    except Exception as e:
        logger.error(f"[Hunyuan3D] Error stopping server: {e}")
    
    finally:
        _server_process = None
        _server_thread = None


# Cached server status for UI (avoids blocking on every panel draw)
_cached_server_status: Optional[bool] = None
_cached_status_time: float = 0
_CACHE_DURATION: float = 10.0  # Cache duration in seconds


def is_server_running(use_cache: bool = False) -> bool:
    """
    Check if the Hunyuan3D server is running and responding.

    Args:
        use_cache: If True, returns cached result for up to 10 seconds (non-blocking for UI)

    Returns:
        True if server is up and responding
    """
    global _cached_server_status, _cached_status_time

    # Return cached value if requested and still valid
    if use_cache and _cached_server_status is not None:
        if time.time() - _cached_status_time < _CACHE_DURATION:
            return _cached_server_status

    # Perform actual check with short timeout
    # The api_server.py doesn't have a /health endpoint, so we check /status/ping
    # which will return 404 but proves the server is running
    result = False
    try:
        url = f"http://{_server_host}:{_server_port}/status/ping"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=0.5) as response:
            # Any response means server is running
            result = True
    except urllib.error.HTTPError as e:
        # 404 or other HTTP errors mean the server IS running (just no such endpoint)
        result = True
    except (urllib.error.URLError, TimeoutError, OSError, ConnectionRefusedError):
        # Connection refused or timeout means server is NOT running
        result = False

    # Cache the result
    _cached_server_status = result
    _cached_status_time = time.time()

    return result


def is_server_running_cached() -> bool:
    """
    Fast non-blocking check using cached server status.
    Use this in UI code (panel draw functions) to avoid freezing.
    
    Returns:
        Cached server status (may be up to 10 seconds stale)
    """
    return is_server_running(use_cache=True)


def refresh_server_status() -> bool:
    """
    Force refresh the server status cache.
    Use this when user explicitly clicks "Check Server".
    
    Returns:
        Current server status (fresh check)
    """
    return is_server_running(use_cache=False)


def get_server_url() -> Optional[str]:
    """
    Get the server URL if running.
    
    Returns:
        Server URL string or None if not running
    """
    if is_server_running():
        return f"http://{_server_host}:{_server_port}"
    return None


def get_server_port() -> int:
    """Get the configured server port."""
    return _server_port


def get_server_host() -> str:
    """Get the configured server host."""
    return _server_host
