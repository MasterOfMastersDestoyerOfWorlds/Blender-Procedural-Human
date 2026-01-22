import logging


class FilenameFilter(logging.Filter):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def filter(self, record):
        return record.pathname.endswith(self.filename)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
