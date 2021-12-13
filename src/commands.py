from schedule import *
from schedule_factory import *

from player import *
from game import *
from metrics import *
from print import *

from optimize_opponents import *
from optimize_seats import *

from helpers import *

def callbackPrintShortOpponents(s : Schedule):
    Print.printPairsMatrix(s)

def callbackPrintOpponents(s : Schedule, filename : str):
    Print.printScheduleByGames(s)
    Print.printScheduleByPlayers(s)
    Print.printOpponentsMatrix(s)
    Print.printPairsMatrix(s)
    Print.printMinMaxPairs(s, [0, 1])
    Print.printMinMaxPairs(s, [6, 7, 8, 9])

    if filename is not None:
        saveSchedule(s, filename)

def callbackPrintSeats(s : Schedule, filename : str):
    # Print.printScheduleByGames(s)
    Print.printSeatsMatrix(s)

    if filename is not None:
        saveSchedule(s, filename)

def optimizeOpponents(conf, filename_opponents, numRuns : int, numIterations : int, expectedPairs : list[int] = [0, 0]):
    conf.validate()
    
    solver = OptimizeOpponents(verbose=False)
    solver.callbackCurrSchedule = lambda s : callbackPrintShortOpponents(s)
    solver.callbackBetterSchedule = lambda s: callbackPrintOpponents(s, filename_opponents)

    # TODO: refactor into expectedPairs list, -1 means no constraint
    solver.expectedZeroPairs = expectedPairs[0]
    solver.expectedSinglePairs = expectedPairs[1]
    s = solver.optimize(conf, numRuns, numIterations)

    print("\n*** Schedule after opponents optimization:")
    callbackPrintOpponents(s, filename_opponents)  

def optimizeSeats(filename_opponents, filename_seats, numRuns, iterations: list[int]):
    s = loadSchedule(filename_opponents)
    s.validate()
    s.generateSlotsFromGames()

    # callbackPrintOpponents(s, None)
    callbackPrintSeats(s, None)

    seats = OptimizeSeats(s, verbose=False)
    seats.callbackBetterSchedule = lambda s : callbackPrintSeats(s, filename_seats)
    seats.optimize(numRuns, iterations)

    print("\n*** Schedule after seats optimization:")
    callbackPrintSeats(s, filename_seats)

def generateParticipants(conf : Configuration, filename_participants):
    print(f"Creating participants: {conf.numPlayers}")
    p = Participants.create(conf.numPlayers)
    saveParticipants(p, filename_participants)


def showSchedule(filename, filename_participants):
    s = loadSchedule(filename)
    s.validate()

    if filename_participants is not None:
        participants = loadParticipants(filename_participants)
        s.setParticipants(participants)
    
    # Print.printScheduleByGames(s)
    Print.printScheduleByPlayers(s)
    Print.printOpponentsMatrix(s)
    Print.printPairsMatrix(s)
    Print.printMinMaxPairs(s, [0, 1])
    Print.printMinMaxPairs(s, [6, 7, 8, 9])
    Print.printSeatsMatrix(s)

    
    print("\n*** MWT-compatible schedule:")
    Print.printMwtSchedule(s)