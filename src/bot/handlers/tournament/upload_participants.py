from dynaconf import settings
from enum import Enum
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler

from ...utils import log
from .common import State, generate_configuration, get_schedule, get_tournament
from mafia_schedule import Participants, Schedule


def create_handlers() -> list:
    """Creates handlers that process `upload_participants` command."""
    return [ConversationHandler(
        entry_points=[
            CommandHandler('upload_participants', upload_participants)
        ],
        states={
            State.WAITING_FOR_PARTICIPANTS: [MessageHandler(filters.ALL, process_participants_list)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
        map_to_parent={
            ConversationHandler.END: State.IDLE
        },
        conversation_timeout=settings.CONVERSATION_TIMEOUT,
        name="show_tournament_conversation",
        persistent=True)]


async def upload_participants(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes upload_participants command."""
    log('upload_participants')
    message = ('Please, enter the list of participants in a single message, '
               'one nickname per line. The nicknames should be exactly like '
               'they are displayed on MWT website. The pairs that you want '
               'to split should be the first ones (players 1 and 2, 3 and 4, etc.')
    await update.message.reply_text(message)
    return State.WAITING_FOR_PARTICIPANTS


async def process_participants_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes the list of participants that the user submitted."""
    log('process_participants_list')
    participants = Participants.createFromNames(update.message.text.split('\n'))
    get_tournament(context)['participants'] = participants.toJson()
    message = ('Thank you! Now you can generate the seating arrangement '
               'if you have not done it yet. If you already did that, '
               'you can generate a text file with nicknames that can '
               'be submitted to MWT.')
    await update.message.reply_text(message)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    return ConversationHandler.END