from telegram.ext import Application

from .handlers import error
from .handlers import debug, info
from .handlers import tournaments


async def post_init(app: Application) -> None:
    """Initializes bot with data and its tasks."""
    app.bot_data.setdefault('tournaments', {})
    app.bot_data.setdefault('version', 1)


def add_handlers(app: Application) -> None:
    """Adds handlers to the bot."""
    # Error handler.
    app.add_error_handler(error.handler)
    # Debug commands.
    for module in [debug, info]:
        app.add_handlers(module.create_handlers())
    # General chat handling.
    for module in [tournaments]:
        app.add_handlers(module.create_handlers())