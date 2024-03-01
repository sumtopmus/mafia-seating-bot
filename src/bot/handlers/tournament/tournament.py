from tkinter import W
from dynaconf import settings
from enum import Enum
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler

from ...utils import log
from .common import State
from .add_tournament import create_handlers as add_tournament_handlers
from .show_tournament import create_handlers as show_tournament_handlers
from .configure_tournament import create_handlers as configure_tournament_handlers
from .upload_participants import create_handlers as upload_participants_handlers
from .generate_seats import create_handlers as generate_seats_handlers
from .show_seats import create_handlers as show_seats_handlers
from .show_stats import create_handlers as show_stats_handlers
from .export_to_mwt import create_handlers as export_to_mwt_handlers


def create_handlers() -> list:
    """Creates handlers that process all tournament conversation."""
    return [ConversationHandler(
        entry_points=add_tournament_handlers() + show_tournament_handlers(),
        states={
            State.IDLE: configure_tournament_handlers() + upload_participants_handlers() + \
                generate_seats_handlers() + show_seats_handlers() + show_stats_handlers() + export_to_mwt_handlers(),
            State.TITLE_READY: configure_tournament_handlers() + upload_participants_handlers() + show_tournament_handlers(),
        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
        name="tournament_conversation",
        persistent=True)]


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    message = (
        'Working with seating assignment for this tournament is canceled. '
        'You can start over.')
    await update.message.reply_text(message)
    return ConversationHandler.END