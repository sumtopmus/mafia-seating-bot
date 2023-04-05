from all_configurations import Configurations
from mafia_schedule.helpers import *

from actions import Actions


def print_help():
    print("Commands: config init load save show_all show_stat show_mwt exit")


def execute_command(actions: Actions, command_string) -> bool:
    if not command_string:
        return False

    params = command_string.split()
    command = params[0]
    params = params[1:] if len(params) > 1 else None

    if command == "exit":
        return True
    elif command == "help":
        print_help()
    elif command == "config":
        actions.setConfig(params)
    elif command == "init":
        actions.initSchedule(params)
    elif command == "load":
        actions.loadSchedule(params)
    elif command == "participants":
        actions.loadParticipants(params)
    elif command == "save":
        actions.saveSchedule(params)
    elif command == "show_all":
        actions.showSchedule(params)
    elif command == "show_rounds":
        actions.showAllRounds(params)
    elif command == "show_players":
        actions.showAllPlayers(params)
    elif command == "show_round":
        actions.showRound(params)
    elif command == "show_stats":
        actions.showStats(params)
    elif command == "show_tables":
        actions.showTables(params)
    elif command == "show_seats":
        actions.showSeats(params)
    elif command == "show_mwt":
        actions.showMwt(params)
    elif command == "show_matrix":
        actions.showScheduleMatrix(params)
    elif command == "show_gender":
        actions.showScheduleGender(params)
    elif command == "check":
        actions.checkSchedule(params)
    elif command == "copy_round":
        actions.copyRound(params)
    elif command == "switch_players":
        actions.switchPlayers(params)
    elif command == "switch_tables":
        actions.switchTables(params)
    else:
        print(f"### Unknown command: {command}")

    return False


def main_loop():
    print("Welcome to interactive mode")

    actions = Actions()

    exit = False
    while not exit:
        command_string = input("\n>> ")
        exit = execute_command(actions, command_string)
