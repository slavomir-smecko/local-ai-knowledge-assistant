import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    exist_ok=True
)


LOG_FILE = LOG_DIR / "rag-assistant.log"


def setup_logging():

    root_logger = logging.getLogger()

    # Prevent duplicate logs with uvicorn reload
    if root_logger.handlers:
        return

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ],
    )


logger = logging.getLogger("rag-assistant")
