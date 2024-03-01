from tkinter import W
from dynaconf import settings
from enum import Enum
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler

from ...utils import log
from .common import State
from telegram import Update
from telegram.ext import ContextTypes


def create_handlers() -> list:
    """Creates handlers that process `add_tournament` command."""
    return [ConversationHandler(
        entry_points=[
            CommandHandler('add_tournament', add_tournament)
        ],
        states={
            State.WAITING_FOR_TITLE: [MessageHandler(~filters.COMMAND, set_title)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
        map_to_parent={
            ConversationHandler.END: State.TITLE_READY
        },
        conversation_timeout=settings.CONVERSATION_TIMEOUT,
        name="add_tournament_conversation",
        persistent=True)]


async def add_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Launches the new tournament sequence."""
    log('add_tournament')
    context.user_data['tournament'] = ""
    context.user_data.setdefault('tournaments', {})
    message = f'Please, enter the name of the tournament.'
    await update.message.reply_text(message)
    return State.WAITING_FOR_TITLE


async def set_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a title."""
    log('set_title')
    context.user_data['tournament'] = update.message.text
    context.user_data['tournaments'].setdefault(update.message.text, {})
    message = f'Click on /configure\_tournament to continue setting up the configuration.'
    await update.message.reply_text(message)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    return ConversationHandler.END