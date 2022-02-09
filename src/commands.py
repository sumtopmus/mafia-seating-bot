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
    Print.print(Print.scheduleByGames(s))
    Print.print(Print.scheduleByPlayers(s))
    Print.print(Print.opponentsMatrix(s))
    Print.print(Print.pairsMatrix(s))
    Print.print(Print.minMaxPairs(s, [0, 1]))
    Print.print(Print.minMaxPairs(s, [6, 7, 8, 9]))

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


def showSchedule(filename, filename_participants):
    path_schedule = getFilePath(filename)
    s = loadSchedule(path_schedule)
    s.validate()

    if filename_participants is not None:
        path_participants = getFilePath(filename_participants)
        participants = loadParticipants(path_participants)
        s.setParticipants(participants)

    # Print.printScheduleByGames(s)
    Print.print(Print.scheduleByPlayers(s))
    Print.print(Print.opponentsMatrix(s))
    Print.print(Print.pairsMatrix(s))
    Print.print(Print.minMaxPairs(s, [0, 1]))
    Print.print(Print.minMaxPairs(s, [6, 7, 8, 9]))
    Print.print(Print.seatsMatrix(s))

    print("\n*** MWT-compatible schedule:")
    Print.print(Print.mwtSchedule(s))
