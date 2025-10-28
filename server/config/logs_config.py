import os
import datetime
import logging
import logging.config
from pathlib import Path
from flask import g, has_app_context

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "../logs"
LOG_PATH.mkdir(parents=True, exist_ok=True)

log_filename = (
    LOG_PATH / f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')}_log_info.log"
)


# # === RequestID filter ===
class RequestIDFilter(logging.Filter):
    def filter(self, record):
        """This code filters request_id from g global per request environment.
        It also applies to non-request logs with providing default value of "-"
        """
        if has_app_context():
            record.request_id = getattr(g, "request_id", "-")
        else:
            record.request_id = "-"
        return True


# === Logging configuration ===
logging_schema = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"request_id_filter": {"()": RequestIDFilter}},
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s [%(request_id)s] %(name)s: %(message)s",
            "datefmt": "%d %b %y %H:%M:%S",
        }
    },
    "handlers": {
        "file_request": {
            "class": "logging.FileHandler",
            "filename": str(log_filename),
            "mode": "a",
            "formatter": "standard",
            "level": "INFO",
            "filters": ["request_id_filter"],
            "encoding": "utf-8",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "__main__": {
            "handlers": ["file_request", "console"],
            "level": "INFO",
            "propagate": False,
        }
    },
    "root": {"handlers": ["file_request", "console"], "level": "INFO"},
}

# Apply configuration
logging.config.dictConfig(logging_schema)

logger = logging.getLogger(__name__)
logger.info(f"Logger initialized at {datetime.datetime.now()}")
