from dynaconf import settings
import io
from telegram import Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler
from telegram.helpers import escape_markdown
from telegram.constants import ParseMode

from mafia_schedule import Print

from utils import log
from .common import get_participants, get_schedule, get_tournament
from .menu import State, construct_seats_menu, construct_show_seats_menu, construct_single_back_button
from mafia_schedule import Participants, Schedule

def create_handlers() -> list:
    """Creates handlers that process `show_seats` command."""
    return [ConversationHandler(
        entry_points=[
            CallbackQueryHandler(show_seats, pattern="^" + State.SHOW_SEATS.name + "$")
        ],
        states={
            State.SHOW_SEATS: [
                CallbackQueryHandler(show_seats, pattern="^" + State.SHOW_SEATS.name + "$"),
                CallbackQueryHandler(show_rounds, pattern="^" + State.SHOWING_ROUNDS.name + "$"),
                CallbackQueryHandler(export_rounds, pattern="^" + State.EXPORTING_ROUNDS.name + "$"),
                CallbackQueryHandler(show_players, pattern="^" + State.SHOWING_PLAYERS.name + "$"),
                CallbackQueryHandler(export_players, pattern="^" + State.EXPORTING_PLAYERS.name + "$"),
                CallbackQueryHandler(show_mwt, pattern="^" + State.SHOWING_MWT.name + "$"),
                CallbackQueryHandler(export_mwt, pattern="^" + State.EXPORTING_MWT.name + "$"),
            ],
        },
        map_to_parent={
            State.SEATS: State.SEATS,
            ConversationHandler.END: ConversationHandler.END
        },
        fallbacks=[
            CallbackQueryHandler(back, pattern="^" + State.SEATS.name + "$"),
            CommandHandler('cancel', cancel)
        ],
        conversation_timeout=settings.CONVERSATION_TIMEOUT,
        name="show_seats_conversation",
        persistent=True)]


async def show_seats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes show seats button press."""
    log('show_seats')
    menu = construct_show_seats_menu(context)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(**menu)
    else:
        await update.message.reply_text(**menu)
    return State.SHOW_SEATS


async def show_seats_after_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Dispalys show seats menu after exporting seats to a file."""
    log('show_seats_after_file')
    menu = construct_show_seats_menu(context)
    message = (
        'Here is the file for you to download. '
        'Is there anything else you want to do with the seating arrangement?')
    menu['text'] = message
    await context.bot.send_message(chat_id=update.effective_chat.id, **menu)
    return State.SHOW_SEATS


async def showing_seats(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    """Showing formatted seating arrangement."""
    log('showing_seats')
    menu = construct_single_back_button(context, State.SHOW_SEATS)
    menu['text'] = message
    await update.callback_query.edit_message_text(**menu, parse_mode=ParseMode.MARKDOWN_V2)
    return


async def show_rounds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes show_rounds command."""
    log('show_rounds')
    await update.callback_query.answer()
    message = escape_markdown('\n'.join(Print.scheduleByGames(
        get_schedule(context, with_participants=True))), version=2)
    await showing_seats(update, context, message)
    return State.SHOW_SEATS


async def export_rounds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When the user presses export rounds button."""
    log('export_rounds')
    await update.callback_query.answer()
    menu = construct_single_back_button(context, State.SHOW_SEATS)
    # TODO: implement
    message = 'This is not supported yet. Please, download in the MWT format.'
    menu['text'] = message
    await update.callback_query.edit_message_text(**menu)
    return State.SHOW_SEATS


async def show_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes show_players command."""
    log('show_players')
    await update.callback_query.answer()
    message = escape_markdown('\n'.join(Print.scheduleByPlayers(
        get_schedule(context, with_participants=True))), version=2)
    await showing_seats(update, context, message)  
    return State.SHOW_SEATS


async def export_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When the user presses export players button."""
    log('export_players')
    await update.callback_query.answer()
    menu = construct_single_back_button(context, State.SHOW_SEATS)
    # TODO: implement
    message = 'This is not supported yet. Please, download in the MWT format.'
    menu['text'] = message
    await update.callback_query.edit_message_text(**menu)
    return State.SHOW_SEATS


async def show_mwt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes show_mwt command."""
    log('show_mwt')
    await update.callback_query.answer()
    message = escape_markdown('\n'.join(Print.mwtSchedule(
        get_schedule(context, with_participants=True))), version=2)
    await showing_seats(update, context, message)  
    return State.SHOW_SEATS


async def export_mwt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When the user presses export to MWT format button."""
    log('export_mwt')
    await update.callback_query.answer()
    message = '\n'.join(Print.mwtSchedule(get_schedule(context, with_participants=True)))
    text_file = io.StringIO(message)
    filename = get_tournament(context)['title'].lower().replace(' ', '-') + '-seats-mwt.txt'
    await context.bot.send_document(
        chat_id=update.effective_chat.id, document=text_file, filename=filename)
    await show_seats_after_file(update, context)
    await update.callback_query.delete_message()
    return State.SHOW_SEATS


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user presses the back button."""
    log('back')
    await update.callback_query.answer()
    menu = construct_seats_menu(context)
    await update.callback_query.edit_message_text(**menu)
    return State.SEATS


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """When a user cancels the process."""
    log('cancel')
    return ConversationHandler.END