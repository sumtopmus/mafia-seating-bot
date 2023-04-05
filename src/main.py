import argparse
import sys
import commands
import interactive
from mafia_schedule.helpers import *
from all_configurations import Configurations
from mafia_schedule import Configuration


class Defaults:
    def __init__(self, conf_name, conf):
        self.conf_name = conf_name
        self.conf = conf

        self.default_opponents = f"{conf_name}_opponents.txt"
        self.default_seats = f"{conf_name}_seats.txt"
        self.default_participants = f"{conf_name}_participants.txt"
        self.default_schedule = f"{conf_name}.txt"
        self.default_mwt = f"{conf_name}_mwt.txt"


def generate_defaults(conf_name: str) -> Defaults:
    conf = Configurations[conf_name] if conf_name in Configurations else None
    defaults = Defaults(conf_name, conf)
    return defaults


def execute_command_interactive(main_parser):
    parser = argparse.ArgumentParser(
        description="Command <interactive> - allows to do advanced processing of schedule in interactive mode",
        parents=[main_parser],
        add_help=False)

    args = parser.parse_args()
    interactive.main_loop()


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
        description="Command <show> - loads and prints the schedule", parents=[main_parser], add_help=False)

    parser.add_argument("--schedule", default=None,
                        help="Schedule filename to show")
    parser.add_argument("--participants", default=None,
                        help="Participants filename")

    parser.add_argument("--show_rounds",
                        action="store_true",
                        help="Show schedule by rounds")
    parser.add_argument("--show_players",
                        action="store_true",
                        help="Show schedule by players")
    parser.add_argument("--show_mwt",
                        action="store_true",
                        help="Show schedule in MWT format")
    parser.add_argument("--all",
                        action="store_true",
                        help="Show everything")
    args = parser.parse_args()

    # if nothing to show - then show all
    if (not args.show_rounds
        and not args.show_players
            and not args.show_mwt):
        args.all = True

    path_schedule = commands.getFilePath(args.schedule)
    schedule = loadSchedule(path_schedule)
    schedule.validate()

    participants = None
    if args.participants is not None:
        path_participants = commands.getFilePath(args.participants)
        participants = loadParticipants(path_participants)

    commands.showSchedule(schedule, participants,
                          args.all or args.show_rounds, args.all or args.show_players, args.all or args.show_mwt)


def execute_command_stats(main_parser):
    parser = argparse.ArgumentParser(
        description="Command <stats> - loads and prints statistics on the schedule", parents=[main_parser], add_help=False)
    parser.add_argument("--schedule", default=None,
                        help="Schedule filename to show")
    parser.add_argument("--participants", default=None,
                        help="Participants filename")

    parser.add_argument("--show_opponent_matrix",
                        action="store_true",
                        help="Show opponent matrix")
    parser.add_argument("--show_opponent_histogram",
                        action="store_true",
                        help="Show pairs histogram")
    parser.add_argument("--show_pairs",
                        action="store_true",
                        help="Show pairs that play too few or too many games")
    parser.add_argument("--show_seats",
                        action="store_true",
                        help="Show seats histogram for every player")
    parser.add_argument("--show_tables",
                        action="store_true",
                        help="Show tables histogram for every player")
    parser.add_argument("--all",
                        action="store_true",
                        help="Show all stats")

    args = parser.parse_args()

    # if nothing to show - then show all
    if (not args.show_opponent_matrix
        and not args.show_opponent_histogram
        and not args.show_pairs
        and not args.show_seats
            and not args.show_tables):
        args.all = True

    path_schedule = commands.getFilePath(args.schedule)
    schedule = loadSchedule(path_schedule)
    schedule.validate()

    participants = None
    if args.participants is not None:
        path_participants = commands.getFilePath(args.participants)
        participants = loadParticipants(path_participants)

    commands.showStats(schedule, participants,
                       showOpponentMatrix=args.all or args.show_opponent_matrix,
                       showOpponentHistogram=args.all or args.show_opponent_histogram,
                       showPairs=args.all or args.show_pairs,
                       showSeats=args.all or args.show_seats,
                       showTables=args.all or args.show_tables)


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


command_handlers = {
    "interactive": execute_command_interactive,
    "opponents": execute_command_opponents,
    "seats": execute_command_seats,
    "participants": execute_command_participants,
    "show": execute_command_show,
    "stats": execute_command_stats,
    "mwt_to_schedule": execute_command_mwt2schedule,
    "schedule_to_mwt": execute_command_schedule2mwt,
}


def main():
    commands_list = [
        f"{command_name}" for command_name in command_handlers]
    command_list_str = " ".join(commands_list)

    parser = argparse.ArgumentParser(
        prog="MafSchedule", description='Mafia schedule processor.',
        epilog=f"Available commands: {command_list_str}.")
    parser.add_argument("command",
                        help=f"List of avaiable commands: {parser.prog} help")

    # parse command only, nothing more!
    cmd_line = sys.argv[1:2]
    args = parser.parse_args(cmd_line)
    command_name = args.command

    if command_name not in command_handlers:
        print(f"Unknown command: {command_name}")
        parser.print_help()
    else:
        handler = command_handlers[command_name]
        handler(parser)


if __name__ == '__main__':
    main()
