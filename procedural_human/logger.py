import logging
from pathlib import Path


class FilenameFilter(logging.Filter):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def filter(self, record):
        return record.pathname.endswith(self.filename)


logging.basicConfig(level=logging.INFO)

_project_root = Path(__file__).resolve().parent.parent
_log_dir = _project_root / ".cursor" / "logs"
_log_dir.mkdir(parents=True, exist_ok=True)
_addon_log_path = _log_dir / "addon.log"

_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
_file_handler = logging.FileHandler(_addon_log_path, encoding="utf-8")
_file_handler.setLevel(logging.INFO)
_file_handler.setFormatter(_formatter)

_root_logger = logging.getLogger()
if not any(
    isinstance(handler, logging.FileHandler)
    and Path(getattr(handler, "baseFilename", "")) == _addon_log_path
    for handler in _root_logger.handlers
):
    _root_logger.addHandler(_file_handler)

logger = logging.getLogger(__name__)
