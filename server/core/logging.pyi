import logging
from _typeshed import Incomplete
from datetime import datetime, timedelta
from logging import LogRecord, Logger
from logging.handlers import BaseRotatingHandler
from pathlib import Path
from typing import Optional, Union

__all__ = ['init_logging']

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
    def __init__(self, filename: str, directory: Optional[StrPath] = None, markup: bool = False, expired_interval: timedelta = ..., maxBytes: int = 1000000.0, backupCount: int = 5, encoding: str = 'utf-8') -> None: ...
    def computeRollover(self) -> datetime: ...
    def format(self, record: LogRecord): ...
    stream: Incomplete
    def shouldRollover(self, record: LogRecord) -> bool: ...
    def delete_expired_logs(self) -> None: ...
    def get_file_name(self, filename: Optional[Union[str, object]] = None, *, base_file: bool = True, time: bool = True, time_str: Optional[str] = None) -> Path: ...
    def doRollover(self) -> bool: ...

class PackagePathFilter(logging.Filter):
    def filter(self, record): ...

def init_logging(level: int, directory: Optional[StrPath] = None) -> Logger: ...
