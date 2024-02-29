# coding=UTF-8

from datetime import datetime, timedelta
from dynaconf import settings
import logging
from telegram import User
import telegram.error
from telegram.ext import Application, ContextTypes


MESSAGE_CLEANUP_JOB = 'message_cleanup'


def log(message: str, level=logging.DEBUG) -> None:
    """Logging/debugging helper."""
    logging.getLogger(__name__).log(level, message)
    if settings.DEBUG:
        print(f'⌚️ {datetime.now().strftime(settings.DATETIME_FORMAT)}: {message}')


def mention(user: User) -> str:
    """Create a user's mention."""
    result = user.mention_markdown(user.name)
    if user.username:
        result += f' ({user.mention_markdown()})'
    return result