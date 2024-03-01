from datetime import datetime
from dynaconf import settings
from enum import Enum
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler

from mafia_schedule import Configuration, OptimizeOpponents, OptimizeSeats, OptimizeTables, Participants, Schedule

from ...utils import log
from .common import generate_configuration, get_participants, get_tournament, State


def create_handlers() -> list:
    """Creates handlers that process `generate_seats` command."""
    return [ConversationHandler(
        entry_points=[
            CommandHandler('generate_seats', generate_seats)
        ],
        states={},
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
        map_to_parent={
            ConversationHandler.END: State.IDLE
        },
        conversation_timeout=settings.CONVERSATION_TIMEOUT,
        name="generate_seats_conversation",
        persistent=True)]


async def generate_seats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes generate_seats command."""
    log('generate_seats')
    message = (
        'I started generating and optimizing the seating assignment. '
        'This can take a while... I will notify you when I am done.')
    bot_message = await update.message.reply_text(message)
    
    # Generating and optimizing the schedule.
    tournament = get_tournament(context)
    config = generate_configuration(tournament)
    config.validate()

    message += '\n\nOptimizing among pairs...'
    num_pairs = tournament['num_pairs']
    schedule = await optimize_opponents(config, num_pairs, context.bot, bot_message, message)
    
    message += ' Done!\nOptimizing among seats...'
    await optimize_seats(schedule, context.bot, bot_message, message)
    
    message += ' Done!\nOptimizing among tables...'
    await optimize_tables(schedule, context.bot, bot_message, message)
    message += ' Done!'
    await context.bot.edit_message_text(
        chat_id=bot_message.chat.id, message_id=bot_message.message_id, text=message)

    # Saving the schedule.
    timestamp = datetime.now().strftime(settings.DATETIME_FORMAT)
    tournament['schedules'] = {timestamp: schedule.toJson()}
    tournament['schedule'] = timestamp

    message = (
        'Seating assignment has been generated! You can view it by clicking on '
        '/show\_seats or export to MWT by clicking on /export\_to\_mwt.')
    await update.message.reply_text(message)
    return ConversationHandler.END


async def report_progress(progress, total, bot, bot_message, message):
    message_with_progress = message + f' ({progress/total:.0%})'
    await bot.edit_message_text(
        chat_id=bot_message.chat.id, message_id=bot_message.message_id, text=message_with_progress)


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


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    """When a user cancels the process."""
    log('cancel')
    return ConversationHandler.END