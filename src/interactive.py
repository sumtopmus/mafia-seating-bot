from config_dir import Configurations
from mafia_schedule.helpers import *

import commands
from actions import Actions


def print_help():
    print("Commands: config init load save show_all show_stat show_mwt exit")


def execute_command(actions: Actions, command_string) -> bool:
    if not command_string:
        return False

    params = command_string.split()
    command = params[0]
    params = params[1:] if len(params) > 1 else None

    # This is debug - delete it
    #print(f"Command string: '{command_string}'")
    #print(f"Command: {command}")
    # if params:
    #    print(f"Params ({len(params)}): {params}")
    # else:
    #    print("No params")

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
    elif command == "save":
        actions.saveSchedule(params)
    elif command == "show_all":
        actions.showSchedule(params)
    elif command == "show_all_rounds":
        actions.showAllRounds(params)
    elif command == "show_round":
        actions.showRound(params)
    elif command == "show_stats":
        actions.showStats(params)
    elif command == "show_seats":
        actions.showSeats(params)
    elif command == "show_mwt":
        actions.showMwt(params)
    elif command == "check":
        actions.checkSchedule(params)
    elif command == "copy_round":
        actions.copyRound(params)
    elif command == "switch_players":
        actions.switchPlayers(params)
    else:
        print(f"### Unknown command: {command}")

    return False


def main_loop(conf):
    print("Welcome to interactive mode")

    actions = Actions()
    actions.conf = conf

    exit = False
    while not exit:
        command_string = input("\n>> ")
        exit = execute_command(actions, command_string)
