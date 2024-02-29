import copy
from datetime import datetime, timedelta
from dynaconf import settings
from telegram.ext import Application

from handlers import error
from handlers import debug, info
from handlers import add_tournament, nickname, show_tournament
import utils


def add_handlers(app: Application) -> None:
    # Error handler.
    app.add_error_handler(error.handler)
    # Debug commands.
    for module in [debug, info]:
        app.add_handlers(module.create_handlers())
    # General chat handling.
    for module in [nickname, add_tournament, show_tournament]:
        app.add_handlers(module.create_handlers())