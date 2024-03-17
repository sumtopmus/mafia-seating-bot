from dynaconf import settings
from enum import Enum
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils import log
from .common import get_participants, get_tournament, validate_configuration, validate_participants, validate_schedule, validate_split_pairs, Validity


State = Enum('State', [
    # Menu state:
    'MAIN_MENU',
    'TOURNAMENTS',
    'TOURNAMENT',
    'CONFIGURATION',
    'SEATS',
    'SHOW_SEATS',
    # Particular states:
    'ADDING_TOURNAMENT',
    'WAITING_FOR_TITLE',
    'WAITING_FOR_NUM_PLAYERS',
    'WAITING_FOR_NUM_TABLES',
    'WAITING_FOR_NUM_ROUNDS',
    'WAITING_FOR_NUM_GAMES',
    'WAITING_FOR_NUM_ATTEMPTS',
    'WAITING_FOR_NUM_PAIRS',
    'WAITING_FOR_PARTICIPANTS',
    'SETTING_PAIRS',
    'FINDING_TOURNAMENT',
    'WAITING_FOR_PLAYER_NUMBER',
    'PICKING_TABLES',
    'WAITING_FOR_ROUND_NUMBER_FOR_TABLES',
    'PICKING_TABLE_PAIR',
    'WAITING_FOR_ROUND_NUMBER_FOR_PLAYERS',
    'WAITING_FOR_PLAYER_NUMBERS',
    # Editing states:
    'EDITING_TITLE',
    'EDITING_PARTICIPANTS',
    'GENERATING_SEATS',
    'AVOIDING_TABLES',
    'SPLITTING_PAIRS',
    'SWAPPING_TABLES',
    'SWAPPING_PLAYERS',
    'RESETTING_IDS',
    'PUBLISHING_TOURNAMENT',
    'DELETING_TOURNAMENT',
    # Viewing states:
    'SHOWING_ROUNDS',
    'EXPORTING_ROUNDS',
    'SHOWING_PLAYERS',
    'EXPORTING_PLAYERS',
    'SHOWING_MWT',
    'EXPORTING_MWT',
    'EXPORTING_SEATS',
    'SHOWING_STATS',
])


def get_validity_suffix(validity) -> str:
    result = ''
    if validity == Validity.INVALID:
        result = ' ⛔️'
    elif validity == Validity.VALID:
        result = ' ✅'
    return result


def construct_main_menu() -> dict:
    log('construct_main_menu')
    text = 'What do you want to do?'
    keyboard = [[
        InlineKeyboardButton("Add Tournament", callback_data=State.ADDING_TOURNAMENT.name),
        InlineKeyboardButton("Show Tournaments", callback_data=State.TOURNAMENTS.name)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return {'text': text, 'reply_markup': reply_markup}


def construct_tournaments_menu(context: ContextTypes.DEFAULT_TYPE) -> dict:
    log('construct_tournaments_menu')
    text = 'Please, pick a tournament:'
    tournaments = context.user_data.get('tournaments', {})
    titles = sorted(tournaments, key=lambda x: tournaments[x]['timestamp'], reverse=True)
    back_button = InlineKeyboardButton('« Back', callback_data=State.MAIN_MENU.name)
    if len(titles) == 0:
        reply_markup = InlineKeyboardMarkup([[back_button]])
        return {'text': 'No tournaments found.', 'reply_markup': reply_markup}
    keyboard = []
    row = []
    for index, title in enumerate(titles):
        row.append(InlineKeyboardButton(title, callback_data=f'{State.TOURNAMENT.name}/{title}'))
        if len(row) == 2:
            keyboard.append(row.copy())
            row = []
        if index == 3:
            break
    row.append(InlineKeyboardButton('Find by name', callback_data=State.FINDING_TOURNAMENT.name))
    if len(row) == 2:
        keyboard.append(row.copy())
        row = []
    row.append(back_button)
    keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    return {'text': text, 'reply_markup': reply_markup}


def construct_tournament_menu(context: ContextTypes.DEFAULT_TYPE) -> dict:
    log('construct_tournament_menu')
    tournament = get_tournament(context)
    state = State(context.user_data['conversation'])
    text = f'What do you want to do with *{tournament['title']}*?'
    configure_button_text = 'Configure' + get_validity_suffix(validate_configuration(context))
    seats_button_text = 'Edit Seats' + get_validity_suffix(validate_schedule(context))
    participants_button_text = 'Upload Participants' + get_validity_suffix(validate_participants(context))
    set_pairs_button_text = 'Set Split Pairs' + get_validity_suffix(validate_split_pairs(context))
    publish_button_text = 'Publish' + (' ✅' if tournament['published'] else '')
    keyboard = [
        [
            InlineKeyboardButton("Edit Title", callback_data=State.EDITING_TITLE.name),
            InlineKeyboardButton(configure_button_text, callback_data=State.CONFIGURATION.name),
        ],
        [
            InlineKeyboardButton(participants_button_text, callback_data=State.EDITING_PARTICIPANTS.name),
            InlineKeyboardButton(set_pairs_button_text, callback_data=State.SETTING_PAIRS.name),
        ],
        [
            InlineKeyboardButton(seats_button_text, callback_data=State.SEATS.name),
            InlineKeyboardButton(publish_button_text, callback_data=State.PUBLISHING_TOURNAMENT.name),  
        ],
        [
            InlineKeyboardButton("Delete ❌", callback_data=State.DELETING_TOURNAMENT.name),
            InlineKeyboardButton("« Back", callback_data=state.name)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return {'text': text, 'reply_markup': reply_markup}


def construct_configuration_menu(context: ContextTypes.DEFAULT_TYPE) -> dict:
    log('construct_configuration_menu')
    tournament = get_tournament(context)    
    text = (
        f'Configuration for *{tournament['title']}*:\n\n'
        f'Number of players: {tournament["config"].get("num_players", "not set")}\n'
        f'Number of tables: {tournament["config"].get("num_tables", "not set")}\n'
        f'Number of rounds: {tournament["config"].get("num_rounds", "not set")}\n'
        f'Number of games: {tournament["config"].get("num_games", "not set")}\n'
        f'Number of attempts: {tournament["config"].get("num_attempts", "not set")}\n'
        f'Number of pairs to split: {tournament["config"].get("num_pairs", "not set")}'
    )    
    num_players_button_text = 'Players' + (' ✅' if 'num_players' in tournament['config'] else '')
    num_tables_button_text = 'Tables' + (' ✅' if 'num_tables' in tournament['config'] else '')
    num_rounds_button_text = 'Rounds' + (' ✅' if 'num_rounds' in tournament['config'] else '')
    num_games_button_text = 'Games' + (' ✅' if 'num_games' in tournament['config'] else '')
    num_attempts_button_text = 'Attempts' + (' ✅' if 'num_attempts' in tournament['config'] else '')
    num_pairs_button_text = 'Split Pairs' + (' ✅' if 'num_pairs' in tournament['config'] else '')
    keyboard = [
        [
            InlineKeyboardButton(num_players_button_text, callback_data=State.WAITING_FOR_NUM_PLAYERS.name),
            InlineKeyboardButton(num_tables_button_text, callback_data=State.WAITING_FOR_NUM_TABLES.name),
        ],
        [
            InlineKeyboardButton(num_rounds_button_text, callback_data=State.WAITING_FOR_NUM_ROUNDS.name),
            InlineKeyboardButton(num_games_button_text, callback_data=State.WAITING_FOR_NUM_GAMES.name),
        ],
        [
            InlineKeyboardButton(num_attempts_button_text, callback_data=State.WAITING_FOR_NUM_ATTEMPTS.name),
            InlineKeyboardButton(num_pairs_button_text, callback_data=State.WAITING_FOR_NUM_PAIRS.name),
        ],
        [
            InlineKeyboardButton("« Back", callback_data=State.TOURNAMENT.name)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return {'text': text, 'reply_markup': reply_markup}


def construct_seats_menu(context: ContextTypes.DEFAULT_TYPE) -> dict:
    log('construct_seats_menu')
    tournament = get_tournament(context)
    text = f'What do you want to do with the seating arrangement?'

    generate_button_text = 'Generate Seats' + get_validity_suffix(validate_schedule(context))
    keyboard = [
        [
            InlineKeyboardButton(generate_button_text, callback_data=State.GENERATING_SEATS.name),
            InlineKeyboardButton("Display/Export", callback_data=State.SHOW_SEATS.name),
        ],
        [
            InlineKeyboardButton("Avoid Tables", callback_data=State.AVOIDING_TABLES.name),
            InlineKeyboardButton("Split Pairs", callback_data=State.SPLITTING_PAIRS.name),
        ],
        [
            InlineKeyboardButton("Swap Tables", callback_data=State.SWAPPING_TABLES.name),
            InlineKeyboardButton("Swap Players", callback_data=State.SWAPPING_PLAYERS.name),
        ],        
        [
            InlineKeyboardButton("Reset Player IDs", callback_data=State.RESETTING_IDS.name),
            InlineKeyboardButton("Statistics", callback_data=State.SHOWING_STATS.name),
        ],
        [
            InlineKeyboardButton("« Back", callback_data=State.TOURNAMENT.name),
        ]        
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return {'text': text, 'reply_markup': reply_markup}


def construct_picking_tables_menu(context: ContextTypes.DEFAULT_TYPE) -> dict:
    log('construct_picking_tables_menu')
    tournament = get_tournament(context)
    participants = get_participants(context)
    player_id = tournament['avoided_tables_player_id']
    avoided_tables = tournament['avoided_tables']
    table_buttons = []
    for index in range(tournament['config']['num_tables']):
        table = chr(ord('A') + index)
        table_buttons.append(InlineKeyboardButton(
            table + (' 🚷' if avoided_tables[index] else ''),
            callback_data=f'{State.PICKING_TABLES.name}/{table}'))
    keyboard = [table_buttons, [InlineKeyboardButton("Done", callback_data=State.SEATS.name)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    nickname = next(player.name for player in participants.people if player.id == player_id)
    text = f'Please, pick tables for {nickname} to avoid.'
    return {'text': text, 'reply_markup': reply_markup}


def construct_picking_tables_pair_menu(context: ContextTypes.DEFAULT_TYPE) -> dict:
    log('construct_picking_tables_pair_menu')
    tournament = get_tournament(context)
    round_id = tournament['swap_tables_round_id']
    tables_pair = tournament['swap_tables_pair']
    table_buttons = []
    for index in range(tournament['config']['num_tables']):
        table = chr(ord('A') + index)
        table_buttons.append(InlineKeyboardButton(
            table + (' 🔄' if index in tables_pair else ''),
            callback_data=f'{State.PICKING_TABLE_PAIR.name}/{table}'))
    keyboard = [table_buttons, [InlineKeyboardButton("Swap", callback_data=State.SEATS.name)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f'Please, pick a pair of tables to swap in Round {round_id+1}.'
    return {'text': text, 'reply_markup': reply_markup}


def construct_show_seats_menu(context: ContextTypes.DEFAULT_TYPE) -> dict:
    log('construct_show_seats_menu')
    text = f'Please, choose how you want to display/export the seating arrangement.'
    keyboard = [
        [
            InlineKeyboardButton("📽️ (by rounds)", callback_data=State.SHOWING_ROUNDS.name),
            InlineKeyboardButton("💾 (by rounds)", callback_data=State.EXPORTING_ROUNDS.name)
        ],
        [
            InlineKeyboardButton("📽️ (by players)", callback_data=State.SHOWING_PLAYERS.name),
            InlineKeyboardButton("💾 (by players)", callback_data=State.EXPORTING_PLAYERS.name),
        ],
        [
            InlineKeyboardButton("📽️ (MWT format)", callback_data=State.SHOWING_MWT.name),
            InlineKeyboardButton("💾 (MWT format)", callback_data=State.EXPORTING_MWT.name)
        ],
        [
            InlineKeyboardButton("« Back", callback_data=State.SEATS.name)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return {'text': text, 'reply_markup': reply_markup}


def construct_single_back_button(context: ContextTypes.DEFAULT_TYPE, state: State) -> dict:
    log('construct_single_back_button')
    keyboard = [[InlineKeyboardButton("« Back", callback_data=state.name)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return {'reply_markup': reply_markup}


def construct_deletion_menu(tournament: dict) -> dict:
    log('construct_deletion_menu')
    text = f'Are you sure you want to delete {tournament["title"]}?'
    keyboard = [[
        InlineKeyboardButton("Yes 🗑️", callback_data=State.DELETING_TOURNAMENT.name),
        InlineKeyboardButton("No 🚫", callback_data=State.TOURNAMENT.name)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return {'text': text, 'reply_markup': reply_markup}