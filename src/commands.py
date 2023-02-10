import os

from mafia_schedule import *
from mafia_schedule.helpers import *
import rendezvouz


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


def optimizeOpponents(conf, filename_opponents, numRuns: int, numIterations: int, expectedPairs: list[int] = [0, 0]):
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


def optimizeSeats(filename_opponents, filename_seats, numRuns, iterations: list[int]):
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


def generateParticipants(conf: Configuration, filename_participants):
    print(f"Creating participants: {conf.numPlayers}")
    p = Participants.create(conf.numPlayers)

    path_participants = getFilePath(filename_participants)
    saveParticipants(p, path_participants)


def showSchedule(schedule: Schedule, participants: Participants):
    if participants:
        schedule.setParticipants(participants)

    Print.print(Print.scheduleByGames(schedule))
    Print.print(Print.scheduleByPlayers(schedule))

    # Print.print(Print.opponentsMatrix(schedule))

    # Print.print(Print.pairsMatrix(schedule))
    # Print.print(Print.minMaxPairs(schedule, [0]))
    # Print.print(Print.minMaxPairs(schedule, [1]))
    # Print.print(Print.minMaxPairs(schedule, [5, 6, 7, 8, 9]))

    # Print.print(Print.minMaxPairs(schedule, [2]))
    # Print.print(Print.minMaxPairs(schedule, [8, 9]))

    # Print.print(Print.seatsMatrix(schedule))


def showRound(schedule: Schedule, participants: Participants, round_index: int):
    if participants:
        schedule.setParticipants(participants)

    round = schedule.rounds[round_index]
    Print.print(Print.roundByGames(schedule, round))


def showAllRounds(schedule: Schedule, participants: Participants):
    if participants:
        schedule.setParticipants(participants)

    Print.print(Print.scheduleByGames(schedule))


def showStats(schedule: Schedule, participants: Participants):
    if participants:
        schedule.setParticipants(participants)

    # temp only - for rendez-vouz
    Print.print(Print.scheduleByGender(schedule))

    if schedule.numTables > 1:
        Print.print(Print.playerTableHistogram(schedule))

    Print.print(Print.minMaxPairs(schedule, [0]))
    # Print.print(Print.minMaxPairs(schedule, [1]))
    # Print.print(Print.minMaxPairs(schedule, [5, 6, 7, 8, 9]))

    Print.print(Print.minMaxPairs(schedule, [2]))
    Print.print(Print.minMaxPairs(schedule, [8, 9]))


def showSeats(schedule: Schedule, participants: Participants):
    if participants:
        schedule.setParticipants(participants)

    Print.print(Print.seatsMatrix(schedule))


def showMwtSchedule(schedule: Schedule, participants: Participants):
    if participants:
        schedule.setParticipants(participants)

    print("\n*** MWT-compatible schedule:")
    Print.print(Print.mwtSchedule(schedule))


def loadMwt(conf: Configuration, filename_mwt: str, filename_schedule: str):
    path_mwt = getFilePath(filename_mwt)
    path_schedule = getFilePath(filename_schedule)

    schedule = loadScheduleFromMwt(conf, path_mwt)
    schedule.validate()
    saveSchedule(schedule, path_schedule)


def saveMwt(filename_schedule: str, filename_mwt: str):
    path_schedule = getFilePath(filename_schedule)
    path_mwt = getFilePath(filename_mwt)

    s = loadSchedule(path_schedule)
    s.validate()

    saveScheduleToMwt(s, path_mwt)


def createRendezVouz(conf: Configuration, filename_schedule: str):
    path_schedule = getFilePath(filename_schedule)
    schedule = rendezvouz.createRendezVouzSchedule(conf)

    # required for opponents matrix
    schedule.generateSlotsFromGames()

    schedule.validate()

    Print.print(Print.scheduleByPlayers(schedule))
    # Print.print(Print.scheduleByGames(schedule))

    Print.print(Print.scheduleByGender(schedule))
    Print.print(Print.playerTableHistogram(schedule))

    Print.print(Print.opponentsMatrix(schedule))
    Print.print(Print.pairsMatrix(schedule))

    opt = OptimizeOpponents(schedule)
    opt.schedule = schedule
    opt.expectedZeroPairs = 0
    opt.expectedSinglePairs = 0
    print(f"\nScore: {opt.scoreFunc():.2f}")
    saveSchedule(schedule, path_schedule)
