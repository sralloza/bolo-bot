import logging
from enum import Enum
from pathlib import Path
from typing import List

from pydantic import BaseSettings


class ValidLoggingLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    def as_python_logging(self):
        return logging._nameToLevel[self.value]


class Settings(BaseSettings):
    class Config:
        env_file = Path(__file__).parent.parent.with_name("settings.env").as_posix()
        env_file_encoding = "utf-8"

    token_bot: str
    sqlalchemy_database_url: str

    log_path: Path = Path(__file__).parent.parent.with_name("logs").joinpath("gale.log")
    logging_level: ValidLoggingLevel = ValidLoggingLevel.INFO
    max_logs: int = 30

    developer: str = "@sralloza"
    developer_id: int = 752192090

    admin_ids: List[int] = []


settings = Settings()
