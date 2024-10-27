import json
import logging
import sys
from datetime import datetime, timedelta, timezone
from logging import LogRecord
from typing import Callable

from app.core.settings import app_settings

logger = logging.getLogger(app_settings.app_title)


class BaseFormatter(logging.Formatter):
    @classmethod
    def _format_log_message(cls, func: Callable) -> Callable:
        def wrapper(self, record: LogRecord) -> str:
            fmt_record = {
                "name": record.name,
                "level": record.levelname,
                "timestamp": datetime.fromtimestamp(record.created, tz=timezone(offset=timedelta(hours=3))).strftime(
                    "%Y-%m-%d %H:%M:%S%z"
                ),
                "message": record.getMessage(),
                "source": f"{record.module}:{record.funcName}:{record.lineno}",
                "exc": func(self, record),
            }
            return json.dumps(fmt_record, ensure_ascii=False)

        return wrapper


def reset_loggers() -> None:
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(BaseFormatter())
    console_handler.setLevel(app_settings.log_level)
    logger.addHandler(console_handler)
    logger.setLevel(app_settings.log_level)
    repeat_loggers = set()
    for log in logging.root.manager.loggerDict.values():
        if not isinstance(log, logging.Logger) or not log.handlers:
            continue
        for handler in log.handlers.copy():
            if log.name in repeat_loggers:
                break
            try:
                log.removeHandler(handler)
            except ValueError:  # in case another thread has already removed it
                pass
            repeat_loggers.add(log.name)
        log.addHandler(console_handler)
        log.setLevel(app_settings.log_level)