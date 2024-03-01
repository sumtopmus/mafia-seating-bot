# coding=UTF-8

from datetime import datetime
from dynaconf import settings
import logging
from telegram import User


MESSAGE_CLEANUP_JOB = 'message_cleanup'


def log(message: str, level=logging.DEBUG) -> None:
    """Logging/debugging helper."""
    logging.getLogger(__name__).log(level, message)
    if settings.DEBUG:
        print(f'⌚️ {datetime.now().strftime(settings.DATETIME_FORMAT)}: {message}')
