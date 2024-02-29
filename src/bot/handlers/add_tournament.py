from tkinter import W
from dynaconf import settings
from enum import Enum
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler

import utils


State = Enum('State', [
    'WAITING_FOR_TITLE',
    'WAITING_FOR_NUM_PLAYERS',
    'WAITING_FOR_NUM_TABLES',
    'WAITING_FOR_NUM_ROUNDS',
    'WAITING_FOR_NUM_GAMES',
    'WAITING_FOR_NUM_ATTEMPTS',
    'WAITING_FOR_NUM_PAIRS'
])


def create_handlers() -> list:
    """Creates handlers that process add_tournament command."""
    return [ConversationHandler(
        entry_points=[
            CommandHandler('add_tournament', add_tournament)
        ],
        states={
            State.WAITING_FOR_TITLE: [MessageHandler(filters.ALL, set_title)],
            State.WAITING_FOR_NUM_PLAYERS: [MessageHandler(filters.ALL, set_num_players)],
            State.WAITING_FOR_NUM_TABLES: [MessageHandler(filters.ALL, set_num_tables)],
            State.WAITING_FOR_NUM_ROUNDS: [MessageHandler(filters.ALL, set_num_rounds)],
            State.WAITING_FOR_NUM_GAMES: [MessageHandler(filters.ALL, set_num_games)],
            State.WAITING_FOR_NUM_ATTEMPTS: [MessageHandler(filters.ALL, set_num_attempts)],
            State.WAITING_FOR_NUM_PAIRS: [MessageHandler(filters.ALL, set_num_pairs)]
        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
        conversation_timeout=settings.CONVERSATION_TIMEOUT,
        name="add_tournament_conversation",
        persistent=True)]


async def add_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Launches the new tournament sequence."""
    utils.log('add_tournament')
    context.user_data['tournament'] = {}
    message = f'Please, enter the name of the tournament.'
    await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
    return State.WAITING_FOR_TITLE


async def set_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a title."""
    utils.log('set_title')
    context.user_data['tournament']['title'] = update.message.text
    message = f'Please, enter the number of players.'
    await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
    return State.WAITING_FOR_NUM_PLAYERS


async def set_num_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of players."""
    utils.log('set_num_players')
    context.user_data['tournament']['num_players'] = update.message.text
    message = f'Please, enter the number of tables.'
    await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
    return State.WAITING_FOR_NUM_TABLES


async def set_num_tables(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of tables."""
    utils.log('set_num_tables')
    context.user_data['tournament']['num_tables'] = update.message.text
    message = f'Please, enter the number of rounds (per table).'
    await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
    return State.WAITING_FOR_NUM_ROUNDS


async def set_num_rounds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of rounds."""
    utils.log('set_num_rounds')
    context.user_data['tournament']['num_rounds'] = update.message.text
    message = f'Please, enter the number of games (total).'
    await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
    return State.WAITING_FOR_NUM_GAMES


async def set_num_games(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of games."""
    utils.log('set_num_games')
    context.user_data['tournament']['num_games'] = update.message.text
    message = f'Please, enter the number of attempts (per player).'
    await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
    return State.WAITING_FOR_NUM_ATTEMPTS


async def set_num_attempts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of attempts."""
    utils.log('set_num_attempts')
    context.user_data['tournament']['num_attempts'] = update.message.text
    message = f'Please, enter the number of pairs to split.'
    await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
    return State.WAITING_FOR_NUM_PAIRS


async def set_num_pairs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a number of pairs."""
    utils.log('set_num_pairs')
    context.user_data['tournament']['num_pairs'] = update.message.text
    context.user_data.setdefault('tournaments', {})
    context.user_data['tournaments'][context.user_data['tournament']['title']] = \
        context.user_data['tournament']
    message = f"Thank you! {context.user_data['tournament']['title']} is now configured."
    await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    utils.log('cancel')
    return ConversationHandler.END