import sys
import commands
import interactive
from config_dir import Configurations
from mafia_schedule import Configuration


def main():
    if len(sys.argv) < 2:
        # TODO: implement dictionary with function pointer to every command
        # Output all command in a generic way: from dictionary keys, not manually like here
        print("Expected opponents|seats|show|load_mwt")
        return

    conf_name = "rv-2023"
    conf = Configurations[conf_name]
    print(f"Configuration name: {conf_name}\n{conf}")

    default_opponents = f"{conf_name}_opponents.txt"
    default_seats = f"{conf_name}_seats.txt"
    default_participants = None  # f"{conf_name}_participants.txt"

    default_schedule = f"{conf_name}.txt"
    default_mwt = f"{conf_name}_mwt.txt"

    command = sys.argv[1]
    print(f"Command: {command}")

    if command == "interactive":
        interactive.main_loop(conf)

    if command == "opponents":
        filename_opponents = sys.argv[2] if len(
            sys.argv) > 2 else default_opponents
        print(f"Output opponents: {filename_opponents}")

        default_numRuns = 20
        default_numIterations = 20 * 1000
        numRuns = int(sys.argv[3]) if len(sys.argv) > 3 else default_numRuns
        numIterations = int(sys.argv[4]) if len(
            sys.argv) > 4 else default_numIterations
        print(f"numRuns: {numRuns}, numIterations: {numIterations}")

        default_zeroPairs = 2  # 0
        default_singlePairs = 0
        expectedZeroPairs = int(sys.argv[5]) if len(
            sys.argv) > 5 else default_zeroPairs
        expectedSinglePairs = int(sys.argv[6]) if len(
            sys.argv) > 6 else default_singlePairs
        print(f"ExpectedZeroPairs: {expectedZeroPairs}")
        print(f"ExpectedSinglePairs: {expectedSinglePairs}")

        commands.optimizeOpponents(conf, filename_opponents, numRuns, numIterations, [
            expectedZeroPairs, expectedSinglePairs])

    if command == "seats":
        filename_opponents = sys.argv[2] if len(
            sys.argv) > 2 else default_opponents
        filename_seats = sys.argv[3] if len(sys.argv) > 3 else default_seats
        print(f"Input opponents: {filename_opponents}")
        print(f"Output seats: {filename_seats}")

        default_numRuns = 30
        default_numIterationsStageOne = 10 * 1000
        default_numIterationsStageTwo = 10 * 1000
        numRuns = int(sys.argv[4]) if len(sys.argv) > 4 else default_numRuns
        numIterationsStageOne = int(sys.argv[5]) if len(
            sys.argv) > 5 else default_numIterationsStageOne
        numIterationsStageTwo = int(sys.argv[6]) if len(
            sys.argv) > 6 else default_numIterationsStageTwo
        listIterations = [numIterationsStageOne, numIterationsStageTwo]
        print(f"numRuns: {numRuns}, iterations: {listIterations}")

        commands.optimizeSeats(filename_opponents, filename_seats,
                               numRuns, listIterations)

    if command == "participants":
        filename_participants = sys.argv[2] if len(
            sys.argv) > 2 else default_participants
        commands.generateParticipants(conf, filename_participants)

    if command == "show" or command == "show_short":

        filename_schedule = sys.argv[2] if len(sys.argv) > 2 else default_seats
        filename_participants = sys.argv[3] if len(
            sys.argv) > 3 else default_participants

        show_full = command == "show"
        if show_full:
            commands.showSchedule(filename_schedule, filename_participants)
        else:
            commands.shortSchedule(filename_schedule, filename_participants)

    if command == "show_mwt":
        filename_schedule = sys.argv[2] if len(
            sys.argv) > 2 else default_schedule
        filename_participants = sys.argv[3] if len(
            sys.argv) > 3 else default_participants
        commands.showMwt(filename_schedule, filename_participants)

    if command == "show_team":
        filename_schedule = sys.argv[2] if len(
            sys.argv) > 2 else default_schedule
        filename_participants = sys.argv[3] if len(
            sys.argv) > 3 else default_participants
        commands.showTeamSchedule(filename_schedule, filename_participants)

    if command == "mwt_to_schedule":
        filename_mwt = sys.argv[2] if len(sys.argv) > 2 else default_mwt
        filename_schedule = sys.argv[3] if len(
            sys.argv) > 3 else default_schedule
        commands.loadMwt(conf, filename_mwt, filename_schedule)

    if command == "schedule_to_mwt":
        filename_schedule = sys.argv[2] if len(
            sys.argv) > 2 else default_schedule
        filename_mwt = sys.argv[3] if len(sys.argv) > 3 else default_mwt
        commands.saveMwt(filename_schedule, filename_mwt)

    if command == "rv":
        filename_schedule = sys.argv[2] if len(
            sys.argv) > 2 else default_schedule
        commands.createRendezVouz(conf, filename_schedule)


if __name__ == '__main__':
    main()
