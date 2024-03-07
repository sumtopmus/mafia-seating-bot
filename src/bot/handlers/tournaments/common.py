from datetime import datetime
from enum import Enum
from telegram.ext import ContextTypes

from ...utils import log
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


def validate_configuration(tournament: dict) -> Validity:
    result = Validity.VALID
    if 'config' not in tournament:
        return Validity.NOT_SET
    for key in ['num_players', 'num_tables', 'num_rounds', 'num_games', 'num_attempts', 'num_pairs']:
        if key not in tournament['config']:
            result = Validity.NOT_SET
    # TODO: check validity of the values
    return result


def get_participants(context: ContextTypes.DEFAULT_TYPE) -> dict:
    """Gets participants from the bot user data."""
    tournament = get_tournament(context)
    if tournament is None:
        return None
    return tournament.get('participants', None)


def get_schedule(context: ContextTypes.DEFAULT_TYPE) -> Schedule:
    """Gets a schedule from the bot user data and transforms dict into the Schedule."""
    tournament = get_tournament(context)
    timestamp = tournament.get('schedule', None)
    if timestamp is None:
        return None
    schedule = Schedule.fromJson(tournament['schedules'][timestamp])
    participants = get_participants(context)
    if participants:
        schedule.setParticipants(Participants.fromJson(participants))
    return schedule


def save_schedule(context: ContextTypes.DEFAULT_TYPE, schedule: Schedule) -> None:
    """Saves the schedule into the bot user data."""
    tournament = get_tournament(context)
    timestamp = datetime.now().isoformat()
    tournament['schedules'] = {timestamp: schedule.toJson()}
    tournament['schedule'] = timestamp
