from schedule import *
from schedule_factory import *

from player import *
from game import *
from metrics import *
from print import *

from optimize_opponents import *
from optimize_seats import *

from helpers import *


filename_opponents = "schedule_opponents.txt"
filename_seats = "schedule_seats.txt"
filename_participants = "participants.txt"

Configurations = {
    "VaWaCa-2017":
        Configuration(numPlayers=25, numTables=2, numRounds=10,
                      numGames=20, numAttempts=8),
    "VaWaCa-2019":
        Configuration(numPlayers=30, numTables=3, numRounds=10,
                      numGames=30, numAttempts=10),
    "MiniTournament12":
        Configuration(numPlayers=12, numTables=1, numRounds=12,
                      numGames=12, numAttempts=10),
    "GG-2021":
        Configuration(numPlayers=36, numTables=3, numRounds=12,
                      numGames=36, numAttempts=10),
}


def demoOptimizeOpponents():
    conf = Configurations["GG-2021"]
    conf.validate()

    opponents = OptimizeOpponents(verbose=False)
    s = opponents.optimize(conf, numRuns=3, numIterations=10 * 1000)

    print("\n*** Schedule after opponents optimization:")
    Print.printScheduleByGames(s)
    Print.printOpponentsMatrix(s)
    Print.printPairsMatrix(s)
    Print.printMinMaxPairs(s, [0, 6, 7, 8, 9])

    saveSchedule(s, filename_opponents)


def demoOptimizeSeats():
    s = loadSchedule(filename_opponents)
    s.generateSlotsFromGames()

    print("\n*** Loaded schedule")
    Print.printScheduleByGames(s)
    Print.printOpponentsMatrix(s)
    Print.printPairsMatrix(s)

    seats = OptimizeSeats(s, verbose=False)
    seats.optimize(numRuns=50, iterations=[30 * 1000, 30 * 1000])

    print("\n*** Schedule after seats optimization:")
    Print.printScheduleByGames(s)
    Print.printSeatsMatrix(s)

    print("\n*** MWT-compatible schedule")
    Print.printMwtSchedule(s)

    saveSchedule(s, filename_seats)


def demoParticipants():
    numPlayers = 36
    p = Participants.create(numPlayers)
    saveParticipants(p, filename_participants)


def demoMwt(filename):
    s = loadSchedule(filename)

    print("\n*** Loaded schedule")
    Print.printScheduleByGames(s)
    Print.printOpponentsMatrix(s)
    Print.printPairsMatrix(s)
    Print.printMinMaxPairs(s, [0, 6, 7, 8, 9])
    
    Print.printSeatsMatrix(s)

    print("\n*** MWT-compatible schedule with IDs:")
    Print.printMwtSchedule(s)

    participants = loadParticipants(filename_participants)

    s.setParticipants(participants)
    print("\n*** MWT-compatible schedule with names:")
    Print.printMwtSchedule(s)


def main():
    # demoOptimizeOpponents()
    demoOptimizeSeats()

    # demoParticipants()
    # demoMwt("schedule_opponents_good.txt")


if __name__ == '__main__':
    main()
