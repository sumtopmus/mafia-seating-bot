import argparse
import sys
import commands
import interactive
from mafia_schedule.helpers import *
from config_dir import Configurations
from mafia_schedule import Configuration


class Defaults:
    def __init__(self, conf_name):
        self.conf_name = conf_name
        if conf_name:
            self.conf = Configurations[conf_name]
        else:
            self.conf = None

        self.default_opponents = f"{conf_name}_opponents.txt"
        self.default_seats = f"{conf_name}_seats.txt"
        self.default_participants = f"{conf_name}_participants.txt"
        self.default_schedule = f"{conf_name}.txt"
        self.default_mwt = f"{conf_name}_mwt.txt"


def generate_defaults(conf_name: str) -> Defaults:
    defaults = Defaults(conf_name)
    return defaults


def execute_command_help(parser):
    parser.print_help()


def execute_command_interactive(main_parser):
    parser = argparse.ArgumentParser(
        description="Command <interactive> - allows to do advanced processing of schedule in interactive mode", parents=[main_parser], add_help=False)
    parser.add_argument(
        "--configuration",
        help="Configuration name from file .configurations")

    args = parser.parse_args()
    defaults = generate_defaults(args.configuration)
    interactive.main_loop(defaults.conf)


def execute_command_opponents(main_parser):
    parser = argparse.ArgumentParser(
        description="Command <opponents> - the first step of schedule generation: optimize player opponents", parents=[main_parser], add_help=False)
    parser.add_argument(
        "--configuration", required=True,
        help="Configuration name from file .configurations")

    parser.add_argument("--output", default=None,
                        help="Opponents schedule filename to save the result to")

    parser.add_argument("--numRuns", type=int,
                        help="Number of optimization attempts",
                        default=20)
    parser.add_argument("--numIterations", type=int,
                        help="Number of iterations in every attempt",
                        default=20 * 1000)
    parser.add_argument("--zeroPairs", type=int,
                        help="Number of pairs that should not play with each other",
                        default=0)
    parser.add_argument("--singlePairs", type=int,
                        help="Number of pairs that should play with each other only once", default=0)
    args = parser.parse_args()
    defaults = generate_defaults(args.configuration)

    filename_opponents = args.output if args.output else defaults.default_opponents
    print(f"Output opponents: {filename_opponents}")

    print(f"numRuns: {args.numRuns}, numIterations: {args.numIterations}")
    print(f"ExpectedZeroPairs: {args.zeroPairs}")
    print(f"ExpectedSinglePairs: {args.singlePairs}")

    commands.optimizeOpponents(defaults.conf, filename_opponents, args.numRuns, args.numIterations, [
        args.zeroPairs, args.singlePairs])


def execute_command_seats(main_parser):
    parser = argparse.ArgumentParser(
        description="Command <seats> - the second step of schedule generation: optimize player seats", parents=[main_parser], add_help=False)
    parser.add_argument(
        "--configuration",
        help="Configuration name from file .configurations")
    parser.add_argument("--input", default=None,
                        help="Opponents schedule filename to start with")
    parser.add_argument("--output", default=None,
                        help="Seats schedule filename to save the result to")
    parser.add_argument("--numRuns", type=int,
                        help="Number of optimization attempts",
                        default=20)
    parser.add_argument("--numIterationsStageOne", type=int,
                        help="Number of optimization attempts",
                        default=10 * 1000)
    parser.add_argument("--numIterationsStageTwo", type=int,
                        help="Number of optimization attempts",
                        default=10 * 1000)
    args = parser.parse_args()
    defaults = generate_defaults(args.configuration)

    filename_opponents = args.input if args.input else defaults.default_opponents
    filename_seats = args.output if args.output else defaults.default_seats
    print(f"Input opponents: {filename_opponents}")
    print(f"Output seats: {filename_seats}")

    listIterations = [args.numIterationsStageOne, args.numIterationsStageTwo]
    print(f"numRuns: {args.numRuns}, iterations: {listIterations}")

    commands.optimizeSeats(filename_opponents, filename_seats,
                           args.numRuns, listIterations)


def execute_command_participants(main_parser):
    parser = argparse.ArgumentParser(
        description="Command <participants> - generate participants file based on configuration", parents=[main_parser], add_help=False)
    parser.add_argument(
        "--configuration",
        help="Configuration name from file .configurations")
    parser.add_argument("--output", default=None,
                        help="Output participants filename")

    args = parser.parse_args()
    defaults = generate_defaults(args.configuration)

    filename_participants = args.output if args.output else defaults.default_participants
    commands.generateParticipants(defaults.conf, filename_participants)


def execute_command_show(main_parser):
    parser = argparse.ArgumentParser(
        description="Command <show> - shows schedule", parents=[main_parser], add_help=False)
    parser.add_argument(
        "--configuration",
        help="Configuration name from file .configurations")
    args = parser.parse_args()
    defaults = generate_defaults(args.configuration)

    filename_schedule = sys.argv[2] if len(
        sys.argv) > 2 else defaults.default_seats
    filename_participants = sys.argv[3] if len(
        sys.argv) > 3 else defaults.default_participants

    path_schedule = commands.getFilePath(filename_schedule)
    schedule = loadSchedule(path_schedule)
    schedule.validate()

    # NB: now participants filename is in default, so you MUST have participants filename to show schedule
    # This might be inconvenient
    participants = None
    if filename_participants is not None:
        path_participants = commands.getFilePath(filename_participants)
        participants = loadParticipants(path_participants)

    commands.showSchedule(schedule, participants)


def execute_command_show_mwt(main_parser):
    parser = argparse.ArgumentParser(
        description="Command <show_mwt> - shows schedule in MWT (comma-based) format", parents=[main_parser], add_help=False)
    parser.add_argument(
        "--configuration",
        help="Configuration name from file .configurations")
    args = parser.parse_args()
    defaults = generate_defaults(args.configuration)

    filename_schedule = sys.argv[2] if len(
        sys.argv) > 2 else defaults.default_schedule
    filename_participants = sys.argv[3] if len(
        sys.argv) > 3 else defaults.default_participants

    path_schedule = commands.getFilePath(filename_schedule)
    schedule = loadSchedule(path_schedule)
    schedule.validate()

    participants = None
    if filename_participants is not None:
        path_participants = commands.getFilePath(filename_participants)
        participants = loadParticipants(path_participants)

    commands.showMwtSchedule(schedule, participants)


def execute_command_show_seats(main_parser):
    parser = argparse.ArgumentParser(
        description="Command <show_seats>", parents=[main_parser], add_help=False)
    parser.add_argument(
        "--configuration",
        help="Configuration name from file .configurations")
    args = parser.parse_args()
    defaults = generate_defaults(args.configuration)

    filename_schedule = sys.argv[2] if len(
        sys.argv) > 2 else defaults.default_schedule
    filename_participants = sys.argv[3] if len(
        sys.argv) > 3 else defaults.default_participants

    path_schedule = commands.getFilePath(filename_schedule)
    schedule = loadSchedule(path_schedule)
    schedule.validate()

    participants = None
    if filename_participants is not None:
        path_participants = commands.getFilePath(filename_participants)
        participants = loadParticipants(path_participants)

    commands.showSeats(schedule, participants)


def execute_command_show_team(main_parser):
    filename_schedule = sys.argv[2] if len(
        sys.argv) > 2 else default_schedule
    filename_participants = sys.argv[3] if len(
        sys.argv) > 3 else default_participants
    commands.showTeamSchedule(filename_schedule, filename_participants)


def execute_command_mwt2schedule(main_parser):
    filename_mwt = sys.argv[2] if len(sys.argv) > 2 else default_mwt
    filename_schedule = sys.argv[3] if len(
        sys.argv) > 3 else default_schedule
    commands.loadMwt(conf, filename_mwt, filename_schedule)


def execute_command_schedule2mwt(main_parser):
    filename_schedule = sys.argv[2] if len(
        sys.argv) > 2 else default_schedule
    filename_mwt = sys.argv[3] if len(sys.argv) > 3 else default_mwt
    commands.saveMwt(filename_schedule, filename_mwt)


def execute_command_rv(main_parser):
    filename_schedule = sys.argv[2] if len(
        sys.argv) > 2 else default_schedule
    commands.createRendezVouz(conf, filename_schedule)


command_handlers = {
    "help": execute_command_help,
    "interactive": execute_command_interactive,
    "opponents": execute_command_opponents,
    "seats": execute_command_seats,
    "participants": execute_command_participants,
    "show": execute_command_show,
    "show_mwt": execute_command_show_mwt,
    "show_seats": execute_command_seats,
    "show_team": execute_command_show_team,
    "mwt_to_schedule": execute_command_mwt2schedule,
    "schedule_to_mwt": execute_command_schedule2mwt,
    "rv": execute_command_rv,
}


def main():
    commands_list = [
        f"{command_name}" for command_name in command_handlers]

    parser = argparse.ArgumentParser(
        prog="MafSchedule", description='Mafia schedule processor.',
        epilog="Available commands: " + " ".join(commands_list))
    parser.add_argument("command",
                        help=f"List of avaiable commands: {parser.prog} help")

    # parse command only, nothing more!
    cmd_line = sys.argv[1:2]
    args = parser.parse_args(cmd_line)
    command_name = args.command

    if command_name not in command_handlers:
        print(f"Unknown command: {command_name}")
        execute_command_help(parser)
    else:
        handler = command_handlers[command_name]
        handler(parser)


if __name__ == '__main__':
    main()
