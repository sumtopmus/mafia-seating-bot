from tkinter import W
from dynaconf import settings
from enum import Enum
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler

from ...utils import log
from .common import State


def create_handlers() -> list:
    """Creates handlers that process `configure_tournament` command."""
    return [ConversationHandler(
        entry_points=[
            CommandHandler('configure_tournament', configure_tournament)
        ],
        states={
            State.WAITING_FOR_NUM_PLAYERS: [MessageHandler(~filters.COMMAND, set_num_players)],
            State.WAITING_FOR_NUM_TABLES: [MessageHandler(~filters.COMMAND, set_num_tables)],
            State.WAITING_FOR_NUM_ROUNDS: [MessageHandler(~filters.COMMAND, set_num_rounds)],
            State.WAITING_FOR_NUM_GAMES: [MessageHandler(~filters.COMMAND, set_num_games)],
            State.WAITING_FOR_NUM_ATTEMPTS: [MessageHandler(~filters.COMMAND, set_num_attempts)],
            State.WAITING_FOR_NUM_PAIRS: [MessageHandler(~filters.COMMAND, set_num_pairs)]
        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
        map_to_parent={
            ConversationHandler.END: State.IDLE
        },
        conversation_timeout=settings.CONVERSATION_TIMEOUT,
        name="configure_tournament_conversation",
        persistent=True)]


async def configure_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Launches the new tournament sequence."""
    log('configure_tournament')
    message = f'Please, enter the number of players.'
    await update.message.reply_text(message)
    return State.WAITING_FOR_NUM_PLAYERS


async def set_num_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of players."""
    log('set_num_players')
    context.user_data['tournaments'][context.user_data['tournament']]['num_players'] = \
        int(update.message.text)
    message = f'Please, enter the number of tables.'
    await update.message.reply_text(message)
    return State.WAITING_FOR_NUM_TABLES


async def set_num_tables(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of tables."""
    log('set_num_tables')
    context.user_data['tournaments'][context.user_data['tournament']]['num_tables'] = \
        int(update.message.text)
    message = f'Please, enter the number of rounds (per table).'
    await update.message.reply_text(message)
    return State.WAITING_FOR_NUM_ROUNDS


async def set_num_rounds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of rounds."""
    log('set_num_rounds')
    context.user_data['tournaments'][context.user_data['tournament']]['num_rounds'] = \
        int(update.message.text)
    message = f'Please, enter the number of games (total).'
    await update.message.reply_text(message)
    return State.WAITING_FOR_NUM_GAMES


async def set_num_games(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of games."""
    log('set_num_games')
    context.user_data['tournaments'][context.user_data['tournament']]['num_games'] = \
        int(update.message.text)
    message = f'Please, enter the number of attempts (per player).'
    await update.message.reply_text(message)
    return State.WAITING_FOR_NUM_ATTEMPTS


async def set_num_attempts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of attempts."""
    log('set_num_attempts')
    context.user_data['tournaments'][context.user_data['tournament']]['num_attempts'] = \
        int(update.message.text)
    message = f'Please, enter the number of pairs to split.'
    await update.message.reply_text(message)
    return State.WAITING_FOR_NUM_PAIRS


async def set_num_pairs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of pairs."""
    log('set_num_pairs')
    context.user_data['tournaments'][context.user_data['tournament']]['num_pairs'] = \
        int(update.message.text)
    message = f"Thank you! {context.user_data['tournament']} is now configured."
    await update.message.reply_text(message)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    return ConversationHandler.END