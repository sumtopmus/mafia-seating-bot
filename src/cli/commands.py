import os

from mafia_schedule import *
from mafia_schedule.helpers import *


def getFilePath(filename: str) -> str:
    if not filename:
        return None

    home = os.path.expanduser("~")
    full_filename = os.path.join(home, filename)
    return full_filename


def callbackPrintShortOpponents(s: Schedule):
    Print.print(Print.pairsMatrix(s))


def callbackPrintOpponents(s: Schedule, path: str):
    # Print.print(Print.scheduleByGames(s))
    # Print.print(Print.scheduleByPlayers(s))
    # Print.print(Print.opponentsMatrix(s))
    Print.print(Print.pairsMatrix(s))

    Print.print(Print.minMaxPairs(s, [0]))
    Print.print(Print.minMaxPairs(s, [5, 6, 7, 8, 9]))

    if path is not None:
        saveSchedule(s, path)


def callbackPrintSeats(s: Schedule, path: str):
    # Print.printScheduleByGames(s)
    Print.print(Print.seatsMatrix(s))

    if path is not None:
        saveSchedule(s, path)


def callbackPrintTables(s: Schedule, path: str):
    Print.print(Print.playerTableHistogram(s))

    if path is not None:
        saveSchedule(s, path)


def optimizeOpponents(conf, filename_opponents: str, numRuns: int, numIterations: int, expectedPairs: list[int] = [0, 0]):
    path_opponents = getFilePath(filename_opponents)
    conf.validate()

    solver = OptimizeOpponents(verbose=False)
    solver.callbackCurrSchedule = lambda s: callbackPrintShortOpponents(s)
    solver.callbackBetterSchedule = lambda s: callbackPrintOpponents(
        s, path_opponents)

    # TODO: refactor into expectedPairs list, -1 means no constraint
    solver.expectedZeroPairs = expectedPairs[0]
    solver.expectedSinglePairs = expectedPairs[1]
    s = solver.optimize(conf, numRuns, numIterations)

    print("\n*** Schedule after opponents optimization:")
    callbackPrintOpponents(s, path_opponents)


def optimizeSeats(filename_opponents: str, filename_seats: str, numRuns: int, iterations: list[int]):
    path_opponents = getFilePath(filename_opponents)
    path_seats = getFilePath(filename_seats)

    s = loadSchedule(path_opponents)
    s.validate()
    s.generateSlotsFromGames()

    # callbackPrintOpponents(s, None)
    callbackPrintSeats(s, None)
    seats = OptimizeSeats(s, verbose=False)
    seats.callbackBetterSchedule = lambda s: callbackPrintSeats(
        s, path_seats)
    seats.optimize(numRuns, iterations)

    print("\n*** Schedule after seats optimization:")
    callbackPrintSeats(s, path_seats)


def optimizeTables(filename_input: str, filename_output: str, numRuns: int, iterations: int):
    path_input = getFilePath(filename_input)
    path_output = getFilePath(filename_output)

    s = loadSchedule(path_input)
    s.validate()

    print("\n*** Schedule before tables optimization:")
    callbackPrintTables(s, path_output)

    tables = OptimizeTables(s, verbose=False)
    tables.callbackBetterSchedule = lambda s: callbackPrintTables(
        s, path_output)
    tables.optimize(numRuns, iterations)

    print("\n*** Schedule after tables optimization:")
    callbackPrintTables(s, path_output)


def showAllConfigurations(configurations):
    print("*** List of all configurations:")
    for name, config in configurations.items():
        print(name)


def showOneConfiguration(configurations, name):
    if name in configurations:
        print(name)
        print(configurations[name])
    else:
        print(f"Configuration not found: {name}")


def generateParticipants(conf: Configuration, filename_participants):
    print(f"Creating participants: {conf.numPlayers}")
    p = Participants.create(conf.numPlayers, "Player_")

    path_participants = getFilePath(filename_participants)
    saveParticipants(p, path_participants)


def showSchedule(schedule: Schedule, participants: Participants,
                 scheduleByRounds: bool, scheduleByPlayers: bool, scheduleMwt: bool):
    if participants:
        schedule.setParticipants(participants)

    if scheduleByRounds:
        Print.print(Print.scheduleByGames(schedule))

    if scheduleByPlayers:
        Print.print(Print.scheduleByPlayers(schedule))

    if scheduleMwt:
        Print.print(Print.mwtSchedule(schedule))


def showSingleRound(schedule: Schedule, participants: Participants, round_index: int):
    if participants:
        schedule.setParticipants(participants)

    round = schedule.rounds[round_index]
    Print.print(Print.roundByGames(schedule, round))


def showStats(schedule: Schedule, participants: Participants,
              showOpponentMatrix: bool, showOpponentHistogram: bool, showPairs: bool, showSeats: bool, showTables: bool):
    if participants:
        schedule.setParticipants(participants)

    if showOpponentMatrix:
        Print.print(Print.opponentsMatrix(schedule))

    if showOpponentHistogram:
        Print.print(Print.pairsMatrix(schedule))

    if showPairs:
        Print.print(Print.minMaxPairs(schedule, [0]))
        Print.print(Print.minMaxPairs(schedule, [1]))
        Print.print(Print.minMaxPairs(schedule, [2]))

        # Print.print(Print.minMaxPairs(schedule, [5, 6, 7, 8, 9]))

        Print.print(Print.minMaxPairs(schedule, [5]))
        Print.print(Print.minMaxPairs(schedule, [6]))
        Print.print(Print.minMaxPairs(schedule, [8, 9]))

    if showSeats:
        Print.print(Print.seatsMatrix(schedule))

    if showTables and schedule.numTables > 1:
        Print.print(Print.playerTableHistogram(schedule))


def mwtToSchedule(conf: Configuration, filename_mwt: str, filename_schedule: str, filename_participants : str):
    path_mwt = getFilePath(filename_mwt)
    path_schedule = getFilePath(filename_schedule)
    path_players = getFilePath(filename_participants)

    schedule = loadScheduleFromMwt(conf, path_mwt)
    schedule.validate()

    if path_schedule is not None:
        saveSchedule(schedule, path_schedule)
    else:
        print("Output schedule filename not specified!")

    if path_players is not None:
        saveParticipants(schedule.participants, path_players)
    else:
        print("Output participants filename not specified!")


def scheduleToMwt(filename_schedule: str, filename_participants: str, filename_mwt: str):
    path_schedule = getFilePath(filename_schedule)
    path_mwt = getFilePath(filename_mwt)

    s = loadSchedule(path_schedule)
    s.validate()

    participants = None
    if filename_participants is not None:
        path_participants = getFilePath(filename_participants)
        participants = loadParticipants(path_participants)
        s.setParticipants(participants)

    saveScheduleToMwt(s, path_mwt)
