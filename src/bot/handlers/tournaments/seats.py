from dynaconf import settings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler
from telegram.helpers import escape_markdown

from utils import log
from mafia_schedule import Configuration, OptimizeOpponents, OptimizeSeats, OptimizeTables, Participants, Schedule
from .menu import State, construct_seats_menu, construct_tournament_menu
from .common import generate_configuration, get_participants, get_schedule, get_tournament, save_participants, save_schedule
from .show_seats import create_handlers as show_seats_handlers

def create_handlers():
    """Creates handlers that process the `Configure Tournament` button press."""
    return [ConversationHandler(
        entry_points=[
            CallbackQueryHandler(edit_seats, pattern="^" + State.SEATS.name + "$")
        ],
        states={
            State.SEATS: [
                CallbackQueryHandler(generate_seats, pattern="^" + State.GENERATING_SEATS.name + "$"),
                CallbackQueryHandler(avoid_table, pattern="^" + State.AVOIDING_TABLE.name + "$"),
                CallbackQueryHandler(split_pairs, pattern="^" + State.SPLITTING_PAIRS.name + "$"),
                CallbackQueryHandler(switch_tables, pattern="^" + State.SWITCHING_TABLES.name + "$"),
                CallbackQueryHandler(switch_players, pattern="^" + State.SWITCHING_PLAYERS.name + "$")
            ] + show_seats_handlers(),
            State.WAITING_FOR_PLAYERS_NUMBERS: [
                MessageHandler(filters.TEXT, switch_players_set_players_numbers)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(back, pattern="^" + State.TOURNAMENT.name + "$"),
            CommandHandler('cancel', cancel)
        ],
        map_to_parent={
            State.TOURNAMENT: State.TOURNAMENT
        },
        name="edit_seats_conversation",
        persistent=True)]


async def edit_seats(update: Update, context: CallbackContext) -> None:
    """Processes edit seats button press."""
    log('edit_seats')
    menu = construct_seats_menu(context)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(**menu)
    else:
        await update.message.reply_text(**menu)
    return State.SEATS


async def generate_seats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes `generate seats` command."""
    log('generate_seats')
    await update.callback_query.answer()
    message = (
        'I started generating and optimizing the seating assignment. '
        'This can take a while... I will notify you when I am done.')
    # keyboard = [[InlineKeyboardButton("Stop", callback_data=State.GENERATING_SEATS.name)]]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(message) #, reply_markup=reply_markup)
    
    # Generating and optimizing the schedule.
    tournament = get_tournament(context)
    log(tournament['config'])
    config = generate_configuration(tournament['config'])
    config.validate()

    message += '\n\nOptimizing among pairs...'
    num_pairs = tournament['config']['num_pairs']
    schedule = await optimize_opponents(config, num_pairs, update, message)

    message += ' Done!\nOptimizing among seats...'
    await optimize_seats(schedule, update, message)
    
    message += ' Done!\nOptimizing among tables...'
    await optimize_tables(schedule, update, message)
    message += ' Done!'
    await update.callback_query.edit_message_text(message, reply_markup=reply_markup)

    # Saving the schedule.
    save_schedule(context, schedule)

    message = 'Seating assignment has been generated!'
    menu = construct_seats_menu(context)
    menu['text'] = message
    await update.callback_query.edit_message_text(**menu)
    return State.SEATS


async def report_progress(progress, total, update, message):
    message_with_progress = message + f' ({progress/total:.0%})'
    keyboard = [[InlineKeyboardButton("Stop", callback_data=State.GENERATING_SEATS.name)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(message_with_progress, reply_markup=reply_markup)
    

async def optimize_opponents(config: Configuration, num_pairs: int, *args) -> Schedule:
    # Optimizing among pairs.
    num_runs = settings.OPPONENTS_OPTIMIZATION.NUM_RUNS
    num_iterations = settings.OPPONENTS_OPTIMIZATION.NUM_ITERATIONS

    solver = OptimizeOpponents(verbose=False)
    solver.expectedZeroPairs = num_pairs
    solver.expectedSinglePairs = 0
    solver.callbackProgress = lambda progress, total: report_progress(progress, total, *args)
        
    schedule = await solver.optimize(config, num_runs, num_iterations)
    schedule.generateSlotsFromGames()

    return schedule


async def optimize_seats(schedule: Schedule, *args):
    # Optimizing among seats.
    num_runs = settings.SEATS_OPTIMIZATION.NUM_RUNS
    num_iterations = settings.SEATS_OPTIMIZATION.NUM_ITERATIONS

    solver = OptimizeSeats(schedule, verbose=False)
    solver.callbackProgress = lambda progress, total: report_progress(progress, total, *args)
    
    await solver.optimize(num_runs, num_iterations)


async def optimize_tables(schedule: Schedule, *args):
    # Optimizing among tables.
    num_runs = settings.TABLES_OPTIMIZATION.NUM_RUNS
    num_iterations = settings.TABLES_OPTIMIZATION.NUM_ITERATIONS

    solver = OptimizeTables(schedule, verbose=False)
    solver.callbackProgress = lambda progress, total: report_progress(progress, total, *args)
    
    await solver.optimize(num_runs, num_iterations)


async def avoid_table(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes avoid_table command."""
    log('avoid_table')
    await update.callback_query.answer()
    message = 'This is not supported yet.'
    menu = construct_seats_menu(context)
    menu['text'] = message
    await update.callback_query.edit_message_text(**menu)
    return State.SEATS


async def split_pairs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes split_pairs command."""
    log('split_pairs')
    await update.callback_query.answer()
    # TODO: implement
    message = 'This is not supported yet.'
    menu = construct_seats_menu(context)
    menu['text'] = message
    await update.callback_query.edit_message_text(**menu)
    return State.SEATS


async def switch_tables(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes switch_tables command."""
    log('switch_tables')
    await update.callback_query.answer()
    # TODO: implement
    message = 'This is not supported yet.'
    menu = construct_seats_menu(context)
    menu['text'] = message
    await update.callback_query.edit_message_text(**menu)
    return State.SEATS


async def switch_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes switch_players command."""
    log('switch_players')
    await update.callback_query.answer()
    participants = [player['name'] for player in get_participants(context)['people']]
    message = 'Please, enter the numbers of the players that you want to switch (space separated).\n\n' + \
        '\n'.join([f'{index+1}. {nickname}' for index, nickname in enumerate(participants)])
    await update.callback_query.edit_message_text(escape_markdown(message))
    return State.WAITING_FOR_PLAYERS_NUMBERS


async def switch_players_set_players_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes switch_players command."""
    log('switch_players_set_players_numbers')
    players_all = get_participants(context)
    players_to_switch = [int(number)-1 for number in update.message.text.split()]
    switch_players_in_schedule(players_all, players_to_switch)
    save_participants(context, players_all)
    edit_seats(update, context)
    return State.SEATS


def switch_players_in_schedule(players_all, players_to_switch):
    """Switches players in the schedule."""
    log('switch_players_in_schedule')
    temp_id = players_all['people'][players_to_switch[0]]['id']
    players_all['people'][players_to_switch[0]]['id'] = players_all['people'][players_to_switch[1]]['id']
    players_all['people'][players_to_switch[1]]['id'] = temp_id


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user presses the back button."""
    log('back')
    await update.callback_query.answer()
    menu = construct_tournament_menu(context)
    await update.callback_query.edit_message_text(**menu)
    return State.TOURNAMENT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    return ConversationHandler.END