from dynaconf import settings
from enum import Enum
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils import log
from .common import get_tournament, validate_configuration, Validity


State = Enum('State', [
    # Menu state:
    'MAIN_MENU',
    'TOURNAMENTS',
    'TOURNAMENT',
    'CONFIGURATION',
    'SEATS',
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
    'FINDING_TOURNAMENT',
    # Editing states:
    'EDITING_TITLE',
    'EDITING_PARTICIPANTS',
    'GENERATING_SEATS',
    'SHOWING_SEATS',
    'EXPORTING_SEATS',
    'SHOWING_STATS',
    'PUBLISHING_TOURNAMENT',
    'DELETING_TOURNAMENT',
])


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
    validity = validate_configuration(tournament)
    validity_suffix = '' if validity == Validity.NOT_SET else ' ✅' if validity == Validity.VALID else ' 🚫'
    configure_button_text = 'Configure' + validity_suffix
    seats_button_text = 'Edit Seats' + (' ✅' if 'schedule' in tournament else '')
    participants_button_text = 'Upload Participants' + (' ✅' if 'participants' in tournament else '')
    publish_button_text = 'Publish' + (' ✅' if tournament['published'] else '')
    keyboard = [
        [
            InlineKeyboardButton("Edit Title", callback_data=State.EDITING_TITLE.name),
            InlineKeyboardButton(configure_button_text, callback_data=State.CONFIGURATION.name),
        ],
        [
            InlineKeyboardButton(seats_button_text, callback_data=State.SEATS.name),
            InlineKeyboardButton(participants_button_text, callback_data=State.EDITING_PARTICIPANTS.name),
        ],
        [
            InlineKeyboardButton(publish_button_text, callback_data=State.PUBLISHING_TOURNAMENT.name),
            InlineKeyboardButton("Delete ❌", callback_data=State.DELETING_TOURNAMENT.name),
        ],
        [
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
    generate_button_text = 'Generate Seats' + (' ✅' if 'schedule' in tournament else '')
    keyboard = [
        [
            InlineKeyboardButton(generate_button_text, callback_data=State.GENERATING_SEATS.name),
            InlineKeyboardButton("Show Seats", callback_data=State.SHOWING_SEATS.name),
        ],
        [
            InlineKeyboardButton("Download Seats", callback_data=State.EXPORTING_SEATS.name),
            InlineKeyboardButton("« Back", callback_data=State.TOURNAMENT.name)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return {'text': text, 'reply_markup': reply_markup}


def construct_deletion_menu(tournament: dict) -> dict:
    log('construct_deletion_menu')
    text = f'Are you sure you want to delete {tournament["title"]}?'
    keyboard = [[
        InlineKeyboardButton("Yes 🗑️", callback_data=State.DELETING_TOURNAMENT.name),
        InlineKeyboardButton("No 🚫", callback_data=State.TOURNAMENT.name)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return {'text': text, 'reply_markup': reply_markup}