from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///data/autminietl.db")
    default_source: str = os.getenv("DEFAULT_SOURCE", "mock")
    schedule_minutes: int = int(os.getenv("SCHEDULE_MINUTES", "30"))
    timezone: str = os.getenv("TIMEZONE", "UTC")
    reports_dir: Path = Path(os.getenv("REPORTS_DIR", "reports"))
    logs_dir: Path = Path(os.getenv("LOGS_DIR", "logs"))


SETTINGS = Settings()
