from dynaconf import settings
from enum import Enum
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler
from telegram.helpers import escape_markdown

from mafia_schedule import Print

from ...utils import log
from .common import get_participants, get_schedule, State
from mafia_schedule import Participants, Schedule

def create_handlers() -> list:
    """Creates handlers that process `show_seats` command."""
    return [ConversationHandler(
        entry_points=[
            CommandHandler('show_seats', show_seats)
        ],
        states={
            State.IDLE: [
                CommandHandler('show_rounds', show_rounds),
                CommandHandler('show_players', show_players),
                CommandHandler('show_mwt', show_mwt),
            ],
        },
        map_to_parent={
            ConversationHandler.END: State.IDLE
        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
        conversation_timeout=settings.CONVERSATION_TIMEOUT,
        name="show_seats_conversation",
        persistent=True)]


async def show_seats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes show_seats command."""
    log('show_seats')
    message = (
        'Choose one of the following options:\n'
        '- /show\_rounds\n'
        '- /show\_players\n'
        '- /show\_mwt\n'
        '- /cancel\n'
    )
    await update.message.reply_text(message)
    return State.IDLE


async def show_rounds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes show_rounds command."""
    log('show_rounds')
    message = escape_markdown('\n'.join(Print.scheduleByGames(get_schedule(context))), version=2)
    await update.message.reply_text(message)
    return State.IDLE


async def show_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes show_players command."""
    log('show_players')
    message = escape_markdown('\n'.join(Print.scheduleByPlayers(get_schedule(context))), version=2)
    await update.message.reply_text(message)
    return State.IDLE


async def show_mwt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes show_mwt command."""
    log('show_mwt')
    message = escape_markdown('\n'.join(Print.mwtSchedule(get_schedule(context))), version=2)
    await update.message.reply_text(message)
    return State.IDLE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    return ConversationHandler.END