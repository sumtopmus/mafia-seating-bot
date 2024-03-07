from dynaconf import settings
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler

from ...utils import log
from .menu import State, construct_main_menu, construct_tournament_menu, construct_tournaments_menu
from .common import get_tournament
from .edit import create_handlers as edit_handlers


def create_handlers() -> list:
    """Creates handlers that show the list of tournaments."""
    return [ConversationHandler(
        entry_points=[
            CallbackQueryHandler(show, pattern="^" + State.TOURNAMENTS.name + "$")
        ],
        states={
            State.TOURNAMENTS: [
                CallbackQueryHandler(find_tournament, pattern="^" + State.FINDING_TOURNAMENT.name + "$")
            ] + edit_handlers(),
            State.FINDING_TOURNAMENT: edit_handlers(),
        },
        fallbacks=[
            CallbackQueryHandler(back, pattern="^" + State.MAIN_MENU.name + "$"),
            CommandHandler('cancel', cancel)
        ],
        map_to_parent={
            State.MAIN_MENU: State.MAIN_MENU
        },
        name="show",
        persistent=True)]


async def show(update: Update, context: CallbackContext) -> None:
    """Processes show command."""
    log('show')    
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(**construct_tournaments_menu(context))
    context.user_data['conversation'] = State.TOURNAMENTS
    return State.TOURNAMENTS


async def find_tournament(update: Update, context: CallbackContext) -> None:
    """Processes find_tournament command."""
    log('find_tournament')
    await update.callback_query.answer()
    message = 'Please, enter the name of the tournament.'
    await update.callback_query.edit_message_text(message)
    return State.FINDING_TOURNAMENT


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user presses the back button."""
    log('back')
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(**construct_main_menu())
    return State.MAIN_MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    message = 'Working with tournaments is canceled. You can start over.'
    await update.message.reply_text(message)
    return ConversationHandler.END