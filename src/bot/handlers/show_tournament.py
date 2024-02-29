from dynaconf import settings
from enum import Enum
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler

import utils


State = Enum('State', ['WAITING_FOR_TITLE'])


def create_handlers() -> list:
    """Creates handlers that process admin's `show_tournament` command."""
    return [ConversationHandler(
        entry_points=[
            CommandHandler('show_tournament', show_tournament)
        ],
        states={
            State.WAITING_FOR_TITLE: [MessageHandler(filters.ALL, tournament_request)],
        },
        fallbacks=[],
        conversation_timeout=settings.CONVERSATION_TIMEOUT,
        name="show_tournament_conversation",
        persistent=True)]


async def show_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Basic admin show_tournament command."""
    utils.log('show_tournament')
    message = f'Please, enter the name of the tournament.'
    await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
    return State.WAITING_FOR_TITLE


async def tournament_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Basic admin tournament_request command."""
    utils.log('tournament_request')
    message = (
        f"Title: {context.user_data['tournament']['title']}"
        f"Number of players: {context.user_data['tournament']['num_players']}"
        f"Number of tables: {context.user_data['tournament']['num_tables']}"
        f"Number of rounds: {context.user_data['tournament']['num_rounds']}"
        f"Number of games: {context.user_data['tournament']['num_games']}"
        f"Number of attempts: {context.user_data['tournament']['num_attempts']}"
        f"Number of pairs: {context.user_data['tournament']['num_pairs']}")
    await context.bot.sendMessage(chat_id=update.message.chat.id, text=message)
    return ConversationHandler.END