from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler

from ...utils import log
from .menu import State, construct_main_menu, construct_tournament_menu
from .common import get_tournament
from .edit import create_handlers as edit_handlers
from .show import create_handlers as show_handlers
# from .configure_tournament import create_handlers as configure_tournament_handlers
# from .upload_participants import create_handlers as upload_participants_handlers
# from .generate_seats import create_handlers as generate_seats_handlers
# from .switch_tables import create_handlers as switch_tables_handlers
# from .show_seats import create_handlers as show_seats_handlers
# from .show_stats import create_handlers as show_stats_handlers
# from .export_to_mwt import create_handlers as export_to_mwt_handlers


def create_handlers() -> list:
    """Creates handlers that process all tournament requests."""
    return [ConversationHandler(
        entry_points= [CommandHandler('start', main_menu)],
        states={
            State.MAIN_MENU: [
                CallbackQueryHandler(add_tournament, pattern="^" + State.ADDING_TOURNAMENT.name + "$")
            ] + show_handlers(),
            State.WAITING_FOR_TITLE: [MessageHandler(~filters.COMMAND, set_title)],
            State.TOURNAMENT: [
                CallbackQueryHandler(back, pattern="^" + State.TOURNAMENTS.name + "$"),
            ] + edit_handlers()
            # State.IDLE: add_tournament_handlers() + edit_handlers() # + \
            #     # configure_tournament_handlers() + upload_participants_handlers() + \
            #     # generate_seats_handlers() + switch_tables_handlers() + show_seats_handlers() + \
            #     # show_stats_handlers() + export_to_mwt_handlers(),
        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
        name="entry_conversation",
        persistent=True)]


async def main_menu(update: Update, context: CallbackContext) -> State:
    """When a user starts the process."""
    log('main_menu')
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(**construct_main_menu())
    else:
        await update.message.reply_text(**construct_main_menu())
    return State.MAIN_MENU


async def add_tournament(update: Update, context: CallbackContext) -> State:
    """Launches the new tournament sequence."""
    log('add_tournament')
    await update.callback_query.answer()
    context.user_data['tournament'] = ""
    context.user_data.setdefault('tournaments', {})
    message = 'Please, enter the name of the tournament.'
    await update.callback_query.edit_message_text(message)
    return State.WAITING_FOR_TITLE


async def set_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a title."""
    log('set_title')
    title = update.message.text
    context.user_data['tournament'] = title
    context.user_data['tournaments'].setdefault(title, {})
    context.user_data['tournaments'][title]['title'] = title
    context.user_data['tournaments'][title]['timestamp'] = datetime.now().isoformat()
    context.user_data['tournaments'][title]['published'] = False
    menu = construct_tournament_menu(get_tournament(context))
    await update.message.reply_text(**menu)
    return State.TOURNAMENT


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user presses the back button after adding a new tournament."""
    log('back')
    await update.callback_query.answer()
    await main_menu(update, context)
    return State.MAIN_MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    message = (
        'Working with seating assignment for this tournament is canceled. '
        'You can start over.')
    await update.message.reply_text(message)
    return ConversationHandler.END