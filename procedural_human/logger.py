import logging
import traceback
from pathlib import Path


class FilenameFilter(logging.Filter):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def filter(self, record):
        return record.pathname.endswith(self.filename)


class CursorErrorFormatter(logging.Formatter):
    def __init__(self, workspace_root: Path):
        super().__init__()
        self.workspace_root = workspace_root

    def _to_workspace_path(self, source_path: str) -> str:
        marker = "\\procedural_human\\"
        idx = source_path.lower().find(marker)
        if idx == -1:
            return source_path
        rel = source_path[idx + 1:]
        return str(self.workspace_root / rel)

    def format(self, record: logging.LogRecord) -> str:
        base = f"{record.levelname}:{record.name}:"
        message = record.getMessage()

        if record.levelno >= logging.ERROR and record.exc_info:
            tb = traceback.extract_tb(record.exc_info[2])
            if tb:
                last_frame = tb[-1]
                path = self._to_workspace_path(last_frame.filename)
                return f"{base} {path}:{last_frame.lineno} : {message}"

        return f"{base}{message}"


_project_root = Path(__file__).resolve().parent.parent
_log_dir = _project_root / ".cursor" / "logs"
_log_dir.mkdir(parents=True, exist_ok=True)
_addon_log_path = _log_dir / "addon.log"

_formatter = CursorErrorFormatter(_project_root)
_file_handler = logging.FileHandler(_addon_log_path, encoding="utf-8")
_file_handler.setLevel(logging.INFO)
_file_handler.setFormatter(_formatter)

def configure_logging():
    logging.basicConfig(level=logging.INFO)
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.setFormatter(_formatter)
    if not any(
        isinstance(handler, logging.FileHandler)
        and Path(getattr(handler, "baseFilename", "")) == _addon_log_path
        for handler in root_logger.handlers
    ):
        root_logger.addHandler(_file_handler)


configure_logging()

logger = logging.getLogger(__name__)
