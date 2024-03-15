from dynaconf import settings
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler
from telegram.helpers import escape_markdown

from utils import log
from mafia_schedule import Configuration, Metrics, OptimizeOpponents, OptimizeSeats, OptimizeTables, Participants, Print, Schedule
from .menu import State, construct_seats_menu, construct_single_back_button, construct_tournament_menu
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
                CallbackQueryHandler(edit_seats, pattern="^" + State.SEATS.name + "$"),
                CallbackQueryHandler(back, pattern="^" + State.TOURNAMENT.name + "$"),
                CallbackQueryHandler(generate_seats, pattern="^" + State.GENERATING_SEATS.name + "$"),
                CallbackQueryHandler(split_pairs_request, pattern="^" + State.SPLITTING_PAIRS.name + "$"),
                CallbackQueryHandler(avoid_table, pattern="^" + State.AVOIDING_TABLE.name + "$"),
                CallbackQueryHandler(switch_tables, pattern="^" + State.SWITCHING_TABLES.name + "$"),
                CallbackQueryHandler(switch_players, pattern="^" + State.SWITCHING_PLAYERS.name + "$"),
                CallbackQueryHandler(reset_ids_request, pattern="^" + State.RESETTING_IDS.name + "$"),
                CallbackQueryHandler(show_stats, pattern="^" + State.SHOWING_STATS.name + "$")
            ] + show_seats_handlers(),
            State.WAITING_FOR_PLAYERS_NUMBERS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, switch_players_set_players_numbers)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', edit_seats)
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
    await update.callback_query.edit_message_text(message) #, reply_markup=reply_markup)

    # Saving the schedule.
    save_schedule(context, schedule)

    # Splitting pairs.
    participants = get_participants(context)
    reset_ids(participants)
    pairs = tournament['pairs']
    split_pairs(participants, pairs)
    save_participants(context, participants)

    message = 'Seating assignment has been generated!'
    menu = construct_seats_menu(context)
    menu['text'] = message
    await update.callback_query.edit_message_text(**menu)
    return State.SEATS


async def report_progress(progress, total, update, message):
    message_with_progress = message + f' ({progress/total:.0%})'
    # keyboard = [[InlineKeyboardButton("Stop", callback_data=State.GENERATING_SEATS.name)]]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(message_with_progress) #, reply_markup=reply_markup)
    

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
    players = [player.name for player in get_participants(context).people]
    message = 'Please, enter the numbers of the players that you want to switch (space separated).\n\n' + \
        '\n'.join([f'{index+1}. {nickname}' for index, nickname in enumerate(players)])
    await update.callback_query.edit_message_text(escape_markdown(message))
    return State.WAITING_FOR_PLAYERS_NUMBERS


async def switch_players_set_players_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes switch_players command."""
    log('switch_players_set_players_numbers')
    participants_all = get_participants(context)
    players_to_switch = [int(number)-1 for number in update.message.text.split()]
    switch_players_in_schedule(participants_all, players_to_switch)
    save_participants(context, participants_all)
    edit_seats(update, context)
    return State.SEATS


def switch_players_in_schedule(participants_all, players_to_switch):
    """Switches players in the schedule."""
    log('switch_players_in_schedule')
    temp_id = participants_all.people[players_to_switch[0]].id
    participants_all.people[players_to_switch[0]].id = participants_all.people[players_to_switch[1]].id
    participants_all.people[players_to_switch[1]].id = temp_id


async def split_pairs_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes split_pairs_request command."""
    log('split_pairs_request')
    await update.callback_query.answer()
    split_pairs(context)    
    message = 'The requested pairs have been split. '
    menu = construct_seats_menu(context)
    menu['text'] = message + menu['text']
    await update.callback_query.edit_message_text(**menu)
    return State.SEATS


def split_pairs(context: ContextTypes.DEFAULT_TYPE):
    """Splits pairs."""
    log('split_pairs')
    participants = get_participants(context)
    pairs = get_tournament(context)['pairs']
    schedule = get_schedule(context)
    schedule.generateSlotsFromGames()
    schedule.setParticipants(participants)
    metrics = Metrics(schedule)
    zero_pairs = [(id, pair) for id in range(schedule.numPlayers) for pair in metrics.calcPlayerPairs(id)[0] if id < pair]
    for index, pair in enumerate(pairs):
        old_ids = [participants.people[pair[i]].id for i in [0, 1]]
        switch_players_in_schedule_by_ids(participants, (old_ids[0], zero_pairs[index][0]))
        switch_players_in_schedule_by_ids(participants, (old_ids[1], zero_pairs[index][1]))
    save_participants(context, participants)


def switch_players_in_schedule_by_ids(participants, pair_to_switch: tuple[int, int]):
    """Switches players in the schedule by their ids."""
    log('switch_players_in_schedule_by_ids')
    for player in participants.people:
        if player.id == pair_to_switch[0]:
            log(f'switching: {player.id} -> {pair_to_switch[1]}')
            player.id = pair_to_switch[1]
        else:
            if player.id == pair_to_switch[1]:
                player.id = pair_to_switch[0]
                log(f'switching: {player.id} -> {pair_to_switch[0]}')


async def reset_ids_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user requests to resets ids of participants."""
    log('reset_ids_request')
    await update.callback_query.answer()
    participants = get_participants(context)
    reset_ids(participants)
    save_participants(context, participants)
    message = 'The player ids were reset. '
    menu = construct_seats_menu(context)
    menu['text'] = message + menu['text']
    await update.callback_query.edit_message_text(**menu)
    return State.SEATS


def reset_ids(participants: Participants) -> State:
    """Resets ids of participants."""
    log('reset_ids')
    for index, player in enumerate(participants.people):
        log(f'{index}: {player}')
        player.id = index


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes show_stats command."""
    log('show_stats')
    await update.callback_query.answer()

    message = ''

    schedule = get_schedule(context)
    schedule.generateSlotsFromGames()
    participants = get_participants(context)
    schedule.setParticipants(participants)
    pairs = get_tournament(context)['pairs']
    players = [f'{index+1}. {player.name} (id: {player.id})' for index, player in enumerate(get_participants(context).people)]

    message += '\n\n' + '> Participants list:\n\n' + '\n'.join(players)
    message += '\n\n' + '> The currently set split pairs are:\n\n' + \
        '\n'.join([f'🚻 👤{pair[0]+1}. {participants[pair[0]]} and 👤{pair[1]+1}. {participants[pair[1]]}' for pair in pairs])
    message += '\n\n' + '> List of players who have no games with each other:\n\n' + \
        '\n'.join(list(Print.minMaxPairs(schedule, [0]))[2:])

    # !!!!
    # log('> Opponents matrix:')
    # log(metrics.calcOpponentsMatrix())
    # message += '\n\n' + '> Opponents matrix:\n\n' + \
    #     '\n'.join(list(Print.opponentsMatrix(schedule))[2:])
    
    # !!! log('> Pairs matrix:')
    # Print.print(Print.pairsMatrix(schedule))

    # log('> Pairs histogram:')
    # log(metrics.calcPairsHistogram())
    # Print.print(Print.pairsHistogram(schedule))    

    # !!! log('> Seats matrix:')
    # Print.print(Print.seatsMatrix(schedule))
    # log(metrics.calcSeatsMatrix())

    # !!! log('> Player table penalties:')
    # Print.print(Print.playerTableHistogram(schedule))
    # log(metrics.calcPlayerTablePenalties())

    menu = construct_single_back_button(context, State.SEATS)
    await update.callback_query.edit_message_text(message, **menu)
    return State.SEATS


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