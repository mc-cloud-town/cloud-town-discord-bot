from _typeshed import Incomplete
from datetime import datetime, timedelta
from logging import LogRecord, Logger
from logging.handlers import BaseRotatingHandler
from pathlib import Path
from typing import Optional, Union

StrPath = Union[Path, str]

class LogTimeRotatingFileHandler(BaseRotatingHandler):
    filename: Incomplete
    directory: Incomplete
    markup: Incomplete
    interval_time: Incomplete
    expired_interval: Incomplete
    maxBytes: Incomplete
    backupCount: Incomplete
    rolloverAt: Incomplete
    def __init__(self, filename: str, directory: Optional[StrPath] = ..., markup: bool = ..., expired_interval: timedelta = ..., maxBytes: int = ..., backupCount: int = ..., encoding: str = ...) -> None: ...
    def computeRollover(self) -> datetime: ...
    def format(self, record: LogRecord): ...
    stream: Incomplete
    def shouldRollover(self, record: LogRecord) -> bool: ...
    def delete_expired_logs(self) -> None: ...
    def get_file_name(self, filename: Optional[Union[str, object]] = ..., *, base_file: bool = ..., time: bool = ..., time_str: Optional[str] = ...) -> Path: ...
    def doRollover(self) -> bool: ...

def init_logging(level: int = ..., directory: Optional[StrPath] = ...) -> Logger: ...
