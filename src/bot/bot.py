from dynaconf import settings
import logging
import os
import pytz
from telegram.constants import ParseMode
from telegram.ext import Application, Defaults, PicklePersistence

from .init import add_handlers


def main() -> None:
    """Runs bot."""
    # Create directory tree structure.
    for path in [settings.DB_PATH, settings.LOG_PATH]:
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    # Set up logging and debugging.
    logging_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(filename=settings.LOG_PATH, level=logging_level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Setup the bot.
    defaults = Defaults(parse_mode=ParseMode.MARKDOWN_V2, tzinfo=pytz.timezone(settings.TIMEZONE))
    persistence = PicklePersistence(filepath=settings.DB_PATH, single_file=False)
    app = Application.builder().token(settings.TOKEN).defaults(defaults)\
        .persistence(persistence).arbitrary_callback_data(True).build()
    # Add handlers.
    add_handlers(app)
    # Start the bot.
    app.run_polling()


if __name__ == "__main__":
    main()