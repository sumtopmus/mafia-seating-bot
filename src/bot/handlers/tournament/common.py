from enum import Enum
from telegram.ext import ContextTypes

from mafia_schedule import Configuration, Participants, Schedule

State = Enum('State', [
    # Meta states:
    'IDLE',
    'TITLE_READY',
    # Particular states:
    'WAITING_FOR_TITLE',
    'WAITING_FOR_NUM_PLAYERS',
    'WAITING_FOR_NUM_TABLES',
    'WAITING_FOR_NUM_ROUNDS',
    'WAITING_FOR_NUM_GAMES',
    'WAITING_FOR_NUM_ATTEMPTS',
    'WAITING_FOR_NUM_PAIRS',
    'WAITING_FOR_PARTICIPANTS',
    # Configuration ready states:
    'GENERATING_SEATS',
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