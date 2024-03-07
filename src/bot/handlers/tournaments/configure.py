from tkinter import W
from dynaconf import settings
from enum import Enum
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler

from ...utils import log
from .menu import State, construct_configuration_menu, construct_tournament_menu
from .common import get_tournament, validate_configuration, Validity


def create_handlers():
    """Creates handlers that process the `Configure Tournament` button press."""
    return [ConversationHandler(
        entry_points=[
            CallbackQueryHandler(configure_tournament, pattern="^" + State.CONFIGURATION.name + "$")
        ],
        states={
            State.CONFIGURATION: [
                CallbackQueryHandler(show_configuration, pattern="^" + State.CONFIGURATION.name + "$"),
                CallbackQueryHandler(
                    lambda update, _: set_parameter_request(update, _, 'players', State.WAITING_FOR_NUM_PLAYERS),
                    pattern="^" + State.WAITING_FOR_NUM_PLAYERS.name + "$"),
                CallbackQueryHandler(
                    lambda update, _: set_parameter_request(update, _, 'tables', State.WAITING_FOR_NUM_TABLES),
                    pattern="^" + State.WAITING_FOR_NUM_TABLES.name + "$"),
                CallbackQueryHandler(
                    lambda update, _: set_parameter_request(update, _, 'rounds', State.WAITING_FOR_NUM_ROUNDS, 'rounds (per table)'),
                    pattern="^" + State.WAITING_FOR_NUM_ROUNDS.name + "$"),
                CallbackQueryHandler(
                    lambda update, _: set_parameter_request(update, _, 'games', State.WAITING_FOR_NUM_GAMES, 'games (total)'),
                    pattern="^" + State.WAITING_FOR_NUM_GAMES.name + "$"),
                CallbackQueryHandler(
                    lambda update, _: set_parameter_request(update, _, 'attempts', State.WAITING_FOR_NUM_ATTEMPTS, 'attempts (per player)'),
                    pattern="^" + State.WAITING_FOR_NUM_ATTEMPTS.name + "$"),
                CallbackQueryHandler(
                    lambda update, _: set_parameter_request(update, _, 'pairs', State.WAITING_FOR_NUM_PAIRS, 'pairs to split'),
                    pattern="^" + State.WAITING_FOR_NUM_PAIRS.name + "$"),
            ],
            State.WAITING_FOR_NUM_PLAYERS: [
                MessageHandler(filters.ALL, lambda update, context: set_parameter(update, context, 'players'))],
            State.WAITING_FOR_NUM_TABLES: [
                MessageHandler(filters.ALL, lambda update, context: set_parameter(update, context, 'tables'))],
            State.WAITING_FOR_NUM_ROUNDS: [
                MessageHandler(filters.ALL, lambda update, context: set_parameter(update, context, 'rounds'))],
            State.WAITING_FOR_NUM_GAMES: [
                MessageHandler(filters.ALL, lambda update, context: set_parameter(update, context, 'games'))],
            State.WAITING_FOR_NUM_ATTEMPTS: [
                MessageHandler(filters.ALL, lambda update, context: set_parameter(update, context, 'attempts'))],
            State.WAITING_FOR_NUM_PAIRS: [
                MessageHandler(filters.ALL, lambda update, context: set_parameter(update, context, 'pairs'))]
        },
        fallbacks=[
            CallbackQueryHandler(back, pattern="^" + State.TOURNAMENT.name + "$"),
            CommandHandler('cancel', cancel)
        ],
        map_to_parent={
            State.TOURNAMENT: State.TOURNAMENT
        },
        name="configure_tournament_conversation",
        persistent=True)]


async def configure_tournament(update: Update, context: CallbackContext) -> None:
    """Processes configure tournament button press."""
    log('configure_tournament')
    await update.callback_query.answer()
    title = context.user_data['tournament']
    context.user_data['tournaments'][title].setdefault('config', {'configured': False, 'valid': True})
    menu = construct_configuration_menu(get_tournament(context))
    await update.callback_query.edit_message_text(**menu)
    return State.CONFIGURATION


async def show_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user wants to see the configuration."""
    log('show_configuration')
    await update.callback_query.answer()
    menu = construct_configuration_menu(get_tournament(context))
    title = context.user_data['tournament']
    message = (
        f'Configuration for *{title}*:\n\n'
        f'*Number of players:* {context.user_data["tournaments"][title]["config"].get("num_players", "not set")}\n'
        f'*Number of tables:* {context.user_data["tournaments"][title]["config"].get("num_tables", "not set")}\n'
        f'*Number of rounds:* {context.user_data["tournaments"][title]["config"].get("num_rounds", "not set")}\n'
        f'*Number of games:* {context.user_data["tournaments"][title]["config"].get("num_games", "not set")}\n'
        f'*Number of attempts:* {context.user_data["tournaments"][title]["config"].get("num_attempts", "not set")}\n'
        f'*Number of pairs to split:* {context.user_data["tournaments"][title]["config"].get("num_pairs", "not set")}'
    )
    menu['text'] = message
    await update.callback_query.edit_message_text(**menu)
    return State.CONFIGURATION


async def set_parameter_request(update: Update, context: ContextTypes.DEFAULT_TYPE,
                      parameter: str, state: State, desc: str = None) -> State:
    """When user wants to set a parameter."""
    log(f'ask_for_num_{parameter}')
    await update.callback_query.answer()
    message = f'Please, enter the number of {desc if desc else parameter}.'
    await update.callback_query.edit_message_text(message)
    return state


async def set_parameter(update: Update, context: ContextTypes.DEFAULT_TYPE,
                      parameter: str) -> State:
    """When a user sets a parameter."""
    log(f'set_num_{parameter}')
    title = context.user_data['tournament']
    context.user_data['tournaments'][title]['config'][f'num_{parameter}'] = \
        int(update.message.text)
    menu = construct_configuration_menu(get_tournament(context))
    await update.message.reply_text(**menu)
    return State.CONFIGURATION


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user presses the back button."""
    log('back')
    await update.callback_query.answer()
    title = context.user_data['tournament']
    if validate_configuration(get_tournament(context)) == Validity.VALID:
        context.user_data['tournaments'][title]['config']['configured'] = True
        context.user_data['tournaments'][title]['config']['valid'] = True
    elif validate_configuration(get_tournament(context)) == Validity.INVALID:
        context.user_data['tournaments'][title]['config']['configured'] = True
        context.user_data['tournaments'][title]['config']['valid'] = False
    else:
        context.user_data['tournaments'][title]['config']['configured'] = False
        context.user_data['tournaments'][title]['config']['valid'] = True
    menu = construct_tournament_menu(context)
    await update.callback_query.edit_message_text(**menu)
    return State.TOURNAMENT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    return ConversationHandler.END