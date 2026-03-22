import logging
from pathlib import Path

from autminietl.config import SETTINGS


def configure_logging() -> None:
    log_dir = Path(SETTINGS.logs_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    logfile = log_dir / "autminietl.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(logfile, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
