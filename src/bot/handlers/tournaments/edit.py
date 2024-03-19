from datetime import datetime
from telegram import Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler
from telegram.helpers import escape_markdown

from utils import log
from .common import get_participants, get_tournament, format_participants, save_participants
from .menu import State, construct_deletion_menu, construct_main_menu, construct_tournament_menu, construct_tournaments_menu
from .configure import create_handlers as configure_handlers
from .seats import create_handlers as seats_handlers
from mafia_schedule import Participants, Schedule


def create_handlers() -> list:
    """Creates handlers that edit a tournament."""
    return [ConversationHandler(
        entry_points=[
            MessageHandler(filters.TEXT & ~filters.COMMAND, set_title),
            CallbackQueryHandler(pick_tournament, pattern="^" + State.TOURNAMENT.name + "/")
        ],
        states={
            State.TOURNAMENT: [
                CallbackQueryHandler(title_edit_request, pattern="^" + State.EDITING_TITLE.name + "$"),
                CallbackQueryHandler(upload_participants_request, pattern="^" + State.EDITING_PARTICIPANTS.name + "$"),
                CallbackQueryHandler(set_pairs_request, pattern="^" + State.SETTING_PAIRS.name + "$"),
                CallbackQueryHandler(publish, pattern="^" + State.PUBLISHING_TOURNAMENT.name + "$"),
                CallbackQueryHandler(delete_request, pattern="^" + State.DELETING_TOURNAMENT.name + "$")
            ] + configure_handlers() + seats_handlers(),
            State.EDITING_TITLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, title_edit)
            ],
            State.WAITING_FOR_PARTICIPANTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, upload_participants)
            ],
            State.SETTING_PAIRS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_pairs)
            ],
            State.DELETING_TOURNAMENT: [
                CallbackQueryHandler(delete, pattern="^" + State.DELETING_TOURNAMENT.name + "$"),
                CallbackQueryHandler(tournament_menu, pattern="^" + State.TOURNAMENT.name + "$")
            ]
        },
        fallbacks=[
            CallbackQueryHandler(back, pattern="^" + State.TOURNAMENTS.name + "$"),
            CallbackQueryHandler(back_to_main_menu, pattern="^" + State.MAIN_MENU.name + "$"),
            CommandHandler('cancel', tournament_menu)
        ],
        map_to_parent={
            State.MAIN_MENU: State.MAIN_MENU,
            State.TOURNAMENTS: State.TOURNAMENTS
        },
        name="edit_tournament_conversation",
        persistent=True)]


async def tournament_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user presses the tournament button."""
    log('tournament_menu')
    menu = construct_tournament_menu(context)
    if update.callback_query:
        await update.callback_query.edit_message_text(**menu)
    else:
        await update.message.reply_text(**menu)
    return State.TOURNAMENT


async def pick_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user presses a tournament button."""
    log('pick_tournament')
    await update.callback_query.answer()
    title = update.callback_query.data.split('/')[1]
    context.user_data['tournament'] = title
    await tournament_menu(update, context)
    return State.TOURNAMENT


async def set_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user adds a title."""
    log('set_title')
    title = update.message.text
    context.user_data['tournament'] = title
    context.user_data['tournaments'].setdefault(title, {})
    tournament = get_tournament(context)
    tournament['title'] = title
    tournament['timestamp'] = datetime.now().isoformat()
    tournament.setdefault('published', False)
    tournament.setdefault('config', {'configured': False, 'valid': True})
    tournament.setdefault('pairs', [])
    await tournament_menu(update, context)
    return State.TOURNAMENT


async def title_edit_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user requests to edit a title."""
    log('edit_title')
    message = 'Please, enter the new title of the tournament.'
    await update.callback_query.edit_message_text(message)
    return State.EDITING_TITLE


async def title_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user edits a title."""
    log('delete')
    old_title = context.user_data['tournament']
    new_title = update.message.text
    if new_title != old_title:
        context.user_data['tournaments'][new_title] = context.user_data['tournaments'][old_title]
        context.user_data['tournaments'][new_title]['title'] = new_title
        del context.user_data['tournaments'][old_title]
        context.user_data['tournament'] = new_title
    await tournament_menu(update, context)
    return State.TOURNAMENT


async def upload_participants_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes upload_participants command."""
    log('upload_participants_request')
    await update.callback_query.answer()
    message = ('Please, enter the list of participants in a single message, '
               'one nickname per line. The nicknames should be exactly like '
               'they are displayed on MWT website.')
    await update.callback_query.edit_message_text(message)
    return State.WAITING_FOR_PARTICIPANTS


async def upload_participants(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes the list of participants that the user submitted."""
    log('upload_participants')
    participants = Participants.createFromNames(
        [nickname.strip() for nickname in update.message.text.split('\n')])
    save_participants(context, participants)
    await tournament_menu(update, context)
    return State.TOURNAMENT


async def set_pairs_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes set_pairs command."""
    log('set_pairs_request')
    await update.callback_query.answer()
    participants = [player.name for player in get_participants(context).people]
    pairs = get_tournament(context)['pairs']
    message = (
        'There are no split pairs currently set. ' if len(pairs) == 0 else \
        'The currently set split pairs are:\n\n' + '\n'.join(
            [f'🚻 👤{participants[pair[0]]} and 👤{participants[pair[1]]}' for pair in pairs]) + '\n\n'
    ) + (
        'Please, enter the pairs of numbers for the players that you want to split '
        '(one pair per line, space separated).\n\n'
    ) + format_participants(context)
    await update.callback_query.edit_message_text(escape_markdown(message))
    return State.SETTING_PAIRS


async def set_pairs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Adds a pair that the user submitted to split list."""
    log('set_pairs')
    pairs = [[int(number)-1 for number in line.split(' ')] for line in update.message.text.split('\n')]
    get_tournament(context)['pairs'] = pairs
    await tournament_menu(update, context)
    return State.TOURNAMENT


async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user publishes the tournament."""
    log('publish')
    title = context.user_data['tournament']
    context.user_data['tournaments'][title]['published'] = True
    context.bot_data['tournaments'][title] = get_tournament(context)
    await update.callback_query.answer(f'{title} is now accessible by everyone.')
    await tournament_menu(update, context)
    return State.TOURNAMENT


async def delete_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user tries to delete the tournament."""
    log('delete_request')
    await update.callback_query.answer()
    menu = construct_deletion_menu(get_tournament(context))
    await update.callback_query.edit_message_text(**menu)
    return State.DELETING_TOURNAMENT


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user tries to delete the tournament."""
    log('delete')
    title = context.user_data['tournament']
    await update.callback_query.answer(f'{title} was successfully deleted.')
    del context.user_data['tournaments'][title]
    menu = construct_main_menu()
    await update.callback_query.edit_message_text(**menu)
    context.user_data['conversation'] = State.MAIN_MENU    
    return State.MAIN_MENU


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user presses the back button."""
    log('back')
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(**construct_tournaments_menu(context))
    return State.TOURNAMENTS


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user presses the back button (to main menu)."""
    log('back_to_main_menu')
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(**construct_main_menu())
    context.user_data['conversation'] = State.MAIN_MENU    
    return State.MAIN_MENU
