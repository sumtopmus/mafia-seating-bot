from all_configurations import Configurations
from mafia_schedule.helpers import *

from actions import Actions


action_handlers = {
    "config": Actions.setConfig,
    "init": Actions.initSchedule,
    "load": Actions.loadSchedule,
    "save": Actions.saveSchedule,
    "participants": Actions.loadParticipants,

    "show": Actions.showSchedule,
    "show_rounds": Actions.showScheduleByRounds,
    "show_players": Actions.showScheduleByPlayers,
    "show_mwt": Actions.showScheduleMwt,
    "show_one_round": Actions.showOneRound,

    "stats": Actions.showStats,
    "stats_opponents": Actions.showStatsOpponents,
    "stats_pairs": Actions.showStatsPairs,
    "stats_tables": Actions.showStatsTables,
    "stats_seats": Actions.showStatsSeats,

    "check": Actions.checkSchedule,
    "copy_round": Actions.copyRound,
    "switch_players": Actions.switchPlayers,
    "switch_tables": Actions.switchTables,
}


def print_help():
    print("Available commands:")
    for command in action_handlers:
        print(f"\t{command}")


def execute_action(actions: Actions, command_string) -> bool:
    if not command_string:
        return False

    params = command_string.split()
    command = params[0]
    params = params[1:] if len(params) > 1 else None

    if command == "exit":
        return True

    if command == "help":
        print_help()
    elif command not in action_handlers:
        print("### Unknown command: {command}. Type 'help' for details.")
    else:
        handler = action_handlers[command]
        handler(actions, params)

    return False


def main_loop():
    print("Welcome to interactive mode")

    actions = Actions()

    exit = False
    while not exit:
        command_string = input("\n>> ")
        exit = execute_action(actions, command_string)
