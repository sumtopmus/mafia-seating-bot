from dynaconf import settings
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler
from telegram.helpers import escape_markdown

from utils import log
from mafia_schedule import Configuration, Metrics, OptimizeOpponents, OptimizeSeats, OptimizeTables, Participants, Print, Schedule
from .menu import State, construct_picking_tables_menu, construct_picking_tables_pair_menu, construct_seats_menu, construct_single_back_button, construct_tournament_menu
from .common import format_participants, generate_configuration, get_participants, get_schedule, get_tables_for_player, get_tournament, save_participants, save_schedule
from .show_seats import create_handlers as show_seats_handlers


def create_handlers():
    """Creates handlers that process the `Edit Seats` button press."""
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
                CallbackQueryHandler(avoid_tables_request, pattern="^" + State.AVOIDING_TABLES.name + "$"),
                CallbackQueryHandler(swap_tables_request, pattern="^" + State.SWAPPING_TABLES.name + "$"),
                CallbackQueryHandler(swap_players_request, pattern="^" + State.SWAPPING_PLAYERS.name + "$"),
                CallbackQueryHandler(reset_ids_request, pattern="^" + State.RESETTING_IDS.name + "$"),
                CallbackQueryHandler(show_stats, pattern="^" + State.SHOWING_STATS.name + "$")
            ] + show_seats_handlers(),
            State.WAITING_FOR_PLAYER_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, pick_tables_to_avoid)
            ],
            State.PICKING_TABLES: [
                CallbackQueryHandler(pick_tables_to_avoid, pattern="^" + State.PICKING_TABLES.name),
                CallbackQueryHandler(avoid_tables, pattern="^" + State.SEATS.name + "$"),
            ],
            State.WAITING_FOR_ROUND_NUMBER_FOR_TABLES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, swap_tables_set_round_number)
            ],
            State.PICKING_TABLE_PAIR: [
                CallbackQueryHandler(swap_tables_pick_tables, pattern="^" + State.PICKING_TABLE_PAIR.name),
                CallbackQueryHandler(swap_tables, pattern="^" + State.SEATS.name + "$"),
            ],
            State.WAITING_FOR_ROUND_NUMBER_FOR_PLAYERS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, swap_players_set_round_number)
            ],
            State.WAITING_FOR_PLAYER_NUMBERS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, swap_players_set_players_numbers)
            ],
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


async def avoid_tables_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user requests to avoid certain tables for a player."""
    log('avoid_tables_request')
    await update.callback_query.answer()
    message = (
        'DISCLAIMER: This feature is experimental and only allows to avoid tables for a single player. '
        'If you have several players with such need, manual swapping is required.\n\n'
        'Enter the number of the player that should avoid certain tables.' + \
        '\n\n' + format_participants(context))
    await update.callback_query.edit_message_text(message)
    return State.WAITING_FOR_PLAYER_NUMBER


async def pick_tables_to_avoid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user picks tables to avoid."""
    log('pick_tables_to_avoid')
    tournament = get_tournament(context)
    if update.message:
        participants = get_participants(context)
        player_id = participants.people[int(update.message.text) - 1].id
        tournament['avoided_tables_player_id'] = player_id
        tournament['avoided_tables'] = [False] * tournament['config']['num_tables']
    else:
        await update.callback_query.answer()
        player_id = tournament['avoided_tables_player_id']
        table_id = ord(update.callback_query.data.split('/')[1]) - ord('A')
        tournament['avoided_tables'][table_id] = not tournament['avoided_tables'][table_id]
    menu = construct_picking_tables_menu(context)
    if update.message:
        await update.message.reply_text(**menu)
    else:
        await update.callback_query.edit_message_text(**menu)
    return State.PICKING_TABLES


async def avoid_tables(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user avoids certain tables for a player."""
    log('avoid_tables')
    await update.callback_query.answer()
    
    tournament = get_tournament(context)
    schedule = get_schedule(context)
    avoided_tables = tournament['avoided_tables']
    player_id = tournament['avoided_tables_player_id']
    original_tables = get_tables_for_player(player_id, schedule)
    available_tables = [table_id for table_id, is_avoided in enumerate(avoided_tables) if not is_avoided]
    next_available_table = 0

    swapped_rounds = []
    for round_index in range(schedule.numRounds):
        table_one_id = original_tables.get(round_index, None)
        if table_one_id is None:
            continue
        if avoided_tables[table_one_id]:
            table_two_id = available_tables[next_available_table]
            swap_tables_in_schedule(schedule, round_index, (table_one_id, table_two_id))
            swapped_rounds.append(round_index)
            next_available_table = (next_available_table + 1) % len(available_tables)
    
    save_schedule(context, schedule)

    menu = construct_seats_menu(context)
    message = 'The tables were changed for rounds ' + ', '.join([str(id+1) for id in swapped_rounds]) + '.\n\n'
    menu['text'] = message + menu['text']
    await update.callback_query.edit_message_text(**menu)
    return State.SEATS


async def swap_tables_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes swap_tables_request command."""
    log('swap_tables_request')
    await update.callback_query.answer()
    tournament = get_tournament(context)
    message = f'Enter the round (from 1 to {tournament['config']['num_rounds']}) where you want to swap the tables.'
    await update.callback_query.edit_message_text(message)
    return State.WAITING_FOR_ROUND_NUMBER_FOR_TABLES


async def swap_tables_set_round_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user sets the round number to swap tables."""
    log('swap_tables_set_round_number')
    round_id = int(update.message.text) - 1
    tournament = get_tournament(context)
    tournament['swap_tables_round_id'] = round_id
    tournament['swap_tables_pair'] = []
    menu = construct_picking_tables_pair_menu(context)
    await update.message.reply_text(**menu)
    return State.PICKING_TABLE_PAIR


async def swap_tables_pick_tables(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user marks a table to swap."""
    log('pick_tables_to_swap')
    await update.callback_query.answer()
    tournament = get_tournament(context)
    table_id = ord(update.callback_query.data.split('/')[1]) - ord('A')
    if table_id in tournament['swap_tables_pair']:
        tournament['swap_tables_pair'].remove(table_id)
    elif len(tournament['swap_tables_pair']) < 2:
        tournament['swap_tables_pair'].append(table_id)
    menu = construct_picking_tables_pair_menu(context)
    await update.callback_query.edit_message_text(**menu)
    return State.PICKING_TABLE_PAIR


async def swap_tables(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes swap_tables command."""
    log('swap_tables')
    await update.callback_query.answer()

    tournament = get_tournament(context)
    round_id = tournament['swap_tables_round_id']
    tables = tournament['swap_tables_pair']
    if len(tables) != 2:
        menu = construct_picking_tables_pair_menu(context)
        message = 'Please, select exactly two tables.'
        menu['text'] = message
        await update.callback_query.edit_message_text(**menu)
        return State.PICKING_TABLE_PAIR
    schedule = get_schedule(context)
    swap_tables_in_schedule(schedule, round_id, tables)
    save_schedule(context, schedule)

    menu = construct_seats_menu(context)
    message = (
        f'The tables {chr(tables[0] + ord('A')) } and {chr(tables[1] + ord('A'))} '
        f'were swapped for Round {str(round_id+1)}.\n\n')
    menu['text'] = message + menu['text']
    await update.callback_query.edit_message_text(**menu)
    return State.SEATS


def swap_tables_in_schedule(schedule: Schedule, round_index: int, tables: tuple[int, int]):
    """Swapes tables in the schedule."""
    log('swap_tables_in_schedule')
    round = schedule.rounds[round_index]
    game_one_id = round.gameIds[tables[0]]
    game_two_id = round.gameIds[tables[1]]
    game_one = schedule.games[game_one_id]
    game_two = schedule.games[game_two_id]
    temp = game_one.players.copy()
    game_one.players = game_two.players.copy()
    game_two.players = temp


async def swap_players_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes swap_players command."""
    log('swap_players_request')
    await update.callback_query.answer()
    tournament = get_tournament(context)
    message = f'Enter the round (from 1 to {tournament['config']['num_rounds']}) where you want to swap the players.'
    await update.callback_query.edit_message_text(message)
    return State.WAITING_FOR_ROUND_NUMBER_FOR_PLAYERS


async def swap_players_set_round_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When user sets the round number to swap players."""
    log('swap_players_set_round_number')
    round_id = int(update.message.text) - 1
    tournament = get_tournament(context)
    tournament['swap_players_round_id'] = round_id
    message = 'Please, enter the numbers of the players that you want to swap (space separated).\n\n' + \
        format_participants(context)
    await update.message.reply_text(escape_markdown(message))
    return State.WAITING_FOR_PLAYER_NUMBERS


async def swap_players_set_players_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """Processes swap_players command."""
    log('swap_players_set_players_numbers')
    players_to_swap = [int(number)-1 for number in update.message.text.split()]
    if len(players_to_swap) != 2:
        message = 'Please, enter exactly two numbers.\n\n' + \
            format_participants(context)
        await update.message.reply_text(message)
        return State.WAITING_FOR_PLAYER_NUMBERS
    
    tournament = get_tournament(context)
    participants = get_participants(context)
    tournament['swap_players_ids'] = [participants.people[index].id for index in players_to_swap]
    participants = get_participants(context)
    nicknames = [participants.people[index].name for index in players_to_swap]
    if swap_players_in_round(context):
        message = (
            f'The players {nicknames[0]} and {nicknames[1]} were succesfully swapped '
            f'in Round {tournament['swap_players_round_id']+1}.')
    else:
        message = (
            f'The players {nicknames[0]} and {nicknames[1]} were swapped '
            f'in Round {tournament['swap_players_round_id']+1} but that made the seating arrangement invalid. '
            'You can swap them back or make the additional swaps to fix the seating arrangement.')
    menu = construct_seats_menu(context)
    menu['text'] = message + '\n\n' + menu['text']
    await update.message.reply_text(**menu)
    return State.SEATS


def swap_players_in_round(context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Swaps players in a round."""
    log('swap_players_in_round')
    tournament = get_tournament(context)
    schedule = get_schedule(context)
    sum_ids = sum(tournament['swap_players_ids'])
    for game_id in schedule.rounds[tournament['swap_players_round_id']].gameIds:
        game = schedule.games[game_id]
        for seat, player_id in enumerate(schedule.games[game_id].players):
            if player_id in tournament['swap_players_ids']:
                game.players[seat] = sum_ids - player_id
    save_schedule(context, schedule)
    return schedule.isValid()


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
        swap_players_in_schedule_by_ids(participants, (old_ids[0], zero_pairs[index][0]))
        swap_players_in_schedule_by_ids(participants, (old_ids[1], zero_pairs[index][1]))
    save_participants(context, participants)


def swap_players_in_schedule_by_ids(participants, pair_to_swap: tuple[int, int]):
    """swapes players in the schedule by their ids."""
    log('swap_players_in_schedule_by_ids')
    for player in participants.people:
        if player.id == pair_to_swap[0]:
            log(f'swaping: {player.id} -> {pair_to_swap[1]}')
            player.id = pair_to_swap[1]
        else:
            if player.id == pair_to_swap[1]:
                player.id = pair_to_swap[0]
                log(f'swaping: {player.id} -> {pair_to_swap[0]}')


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