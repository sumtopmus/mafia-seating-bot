from datetime import datetime
from enum import Enum
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from utils import log
from mafia_schedule import Configuration, Participants, Schedule


Validity = Enum('Validity', [
    'NOT_SET',
    'VALID',
    'INVALID'
])


def generate_configuration(bot_dict: dict) -> Configuration:
    """Generates a configuration from a dictionary."""
    return Configuration(
        numPlayers=bot_dict['num_players'],
        numTables=bot_dict['num_tables'],
        numRounds=bot_dict['num_rounds'],
        numGames=bot_dict['num_games'],
        numAttempts=bot_dict['num_attempts']
    )


def get_tournament(context: ContextTypes.DEFAULT_TYPE) -> dict:
    """Gets a tournament from the bot user data."""
    title = context.user_data.get('tournament', None)
    if title is None:
        return None
    return context.user_data['tournaments'][title]


def get_participants(context: ContextTypes.DEFAULT_TYPE) -> Participants:
    """Gets participants from the bot user data."""
    tournament = get_tournament(context)
    if tournament is None:
        return None
    participants = tournament.get('participants', None)
    if participants is None:
        return None
    return Participants.fromJson(participants)


def format_participants(context: ContextTypes.DEFAULT_TYPE) -> str:
    """Formats participants into a string."""
    participants = get_participants(context)
    players = [f'{index+1}. {player.name}' for index, player in enumerate(participants.people)]
    return escape_markdown('\n'.join(players))


def save_participants(context: ContextTypes.DEFAULT_TYPE, participants: Participants) -> None:
    """Saves participants into the bot user data."""
    tournament = get_tournament(context)
    tournament['participants'] = participants.toJson()


def get_schedule(context: ContextTypes.DEFAULT_TYPE, with_participants=False) -> Schedule:
    """Gets a schedule from the bot user data and transforms dict into the Schedule."""
    tournament = get_tournament(context)
    timestamp = tournament.get('schedule', None)
    if timestamp is None:
        return None
    schedule = Schedule.fromJson(tournament['schedules'][timestamp])
    if with_participants:
        participants = get_participants(context)
        schedule.setParticipants(participants)
    return schedule


def save_schedule(context: ContextTypes.DEFAULT_TYPE, schedule: Schedule) -> None:
    """Saves the schedule into the bot user data."""
    tournament = get_tournament(context)
    timestamp = datetime.now().isoformat()
    tournament['schedules'] = {timestamp: schedule.toJson()}
    tournament['schedule'] = timestamp


def get_tables_for_player(player_id: int, schedule: Schedule) -> dict:
    """Gets tables for a player."""
    tables = {}
    for round_id, round in enumerate(schedule.rounds):
        for table_id, game_id in enumerate(round.gameIds):
            game = schedule.games[game_id]
            assert game.id == game_id
            if player_id in game.players:
                tables[round_id] = table_id
                break
    return tables


def validate_configuration(context: ContextTypes.DEFAULT_TYPE) -> Validity:
    tournament = get_tournament(context)
    if 'config' not in tournament:
        return Validity.NOT_SET
    result = Validity.VALID
    for key in ['num_players', 'num_tables', 'num_rounds', 'num_games', 'num_attempts', 'num_pairs']:
        if key not in tournament['config']:
            result = Validity.NOT_SET
    if result == Validity.NOT_SET:
        return Validity.NOT_SET
    config = generate_configuration(tournament['config'])
    if not config.isValid():
        return Validity.INVALID
    return Validity.VALID


def validate_schedule(context: ContextTypes.DEFAULT_TYPE) -> Validity:
    tournament = get_tournament(context)
    if 'schedule' not in tournament:
        return Validity.NOT_SET
    schedule = get_schedule(context)
    if not schedule.isValid():
        return Validity.INVALID
    return Validity.VALID


def validate_participants(context: ContextTypes.DEFAULT_TYPE) -> Validity:
    tournament = get_tournament(context)
    participants = get_participants(context)
    if participants is None:
        return Validity.NOT_SET
    if len(participants.people) != tournament['config']['num_players']:
        return Validity.INVALID
    else:
        return Validity.VALID
    

def validate_split_pairs(context: ContextTypes.DEFAULT_TYPE) -> Validity:
    tournament = get_tournament(context)
    if 'num_pairs' not in tournament['config']:
        return Validity.NOT_SET
    if len(tournament.get('pairs', [])) == tournament['config']['num_pairs']:
        return Validity.VALID
    else:
        return Validity.INVALID
