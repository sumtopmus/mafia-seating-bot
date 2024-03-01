from dynaconf import settings
from enum import Enum
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler

from ...utils import log
from .common import State

def create_handlers() -> list:
    """Creates handlers that process `show_tournament` command."""
    return [ConversationHandler(
        entry_points=[
            CommandHandler('show_tournament', show_tournament)
        ],
        states={
            State.WAITING_FOR_TITLE: [MessageHandler(filters.ALL, get_tournament_by_title)],
        },
        map_to_parent={
            ConversationHandler.END: State.IDLE
        },        
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
        conversation_timeout=settings.CONVERSATION_TIMEOUT,
        name="show_tournament_conversation",
        persistent=True)]


async def show_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes show_tournament command."""
    log('show_tournament')
    message = f'Please, enter the name of the tournament.'
    await update.message.reply_text(message)
    return State.WAITING_FOR_TITLE


async def get_tournament_by_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """When a users enters the tournament title."""
    log('get_tournament_by_title')
    title = update.message.text
    context.user_data['tournament'] = title
    message = (
        f"*Title:* {title}\n"
        f"*Number of players:* {context.user_data['tournaments'][title]['num_players']}\n"
        f"*Number of tables:* {context.user_data['tournaments'][title]['num_tables']}\n"
        f"*Number of rounds:* {context.user_data['tournaments'][title]['num_rounds']}\n"
        f"*Number of games:* {context.user_data['tournaments'][title]['num_games']}\n"
        f"*Number of attempts:* {context.user_data['tournaments'][title]['num_attempts']}\n"
        f"*Number of pairs:* {context.user_data['tournaments'][title]['num_pairs']}\n")
    await update.message.reply_text(message)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    return ConversationHandler.END