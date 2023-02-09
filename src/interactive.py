from config_dir import Configurations
from mafia_schedule.helpers import *

import commands

g_conf = None
g_schedule = None
g_participants = None
g_filename = None


def print_help():
    print("Commands: config load save show exit")


def set_config(params):
    if not params:
        print(g_conf)

    conf_name = params[0]
    g_conf = Configurations[conf_name]
    print(f"Configuration name: {conf_name}\n{g_conf}")
    print(g_conf)


def do_load(params):
    filename = params[0]
    path = commands.getFilePath(filename)
    g_schedule = loadSchedule(path)


def do_save(params):
    if not g_schedule:
        print("### No schedule, nothing to save")

    filename = params[0]
    path = commands.getFilePath(filename)
    saveSchedule(g_schedule, path)


def do_show(params):
    print("TBD")
    # commands.showSchedule()


def parse_command(command_string) -> bool:
    if not command_string:
        return False

    params = command_string.split()
    command = params[0]
    params = params[1:] if len(params) > 1 else None

    # This is debug - delete it
    print(f"Command string: '{command_string}'")
    print(f"Command: {command}")
    if params:
        print(f"Params ({len(params)}): {params}")
    else:
        print("No params")

    if command == "exit":
        return True
    elif command == "help":
        print_help()
    elif command == "config":
        set_config(params)
    elif command == "load":
        do_load(params)
    elif command == "save":
        do_save(params)
    elif command == "show":
        do_show(params)
    else:
        print(f"### Unknown command: {command}")

    return False


def main_loop(conf):
    print("Welcome to interactive mode")
    g_conf = conf

    exit = False
    while not exit:
        command_string = input(">> ")
        exit = parse_command(command_string)
