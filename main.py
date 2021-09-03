from schedule import *
from schedule_factory import *

from player import *
from game import *
from metrics import *
from print import *

from optimize_opponents import *
from optimize_seats import *

from helpers import *

import sys

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

    "VaWaCa-2021":
        Configuration(numPlayers=36, numTables=3, numRounds=12,
                      numGames=36, numAttempts=10),
}


def demoOptimizeOpponents(conf, filename):
    conf.validate()

    opponents = OptimizeOpponents(verbose=False)
    s = opponents.optimize(conf, numRuns=20, numIterations=20 * 1000)

    print("\n*** Schedule after opponents optimization:")
    Print.printScheduleByGames(s)
    Print.printScheduleByPlayers(s)
    Print.printOpponentsMatrix(s)
    Print.printPairsMatrix(s)
    Print.printMinMaxPairs(s, [0, 6, 7, 8, 9])

    saveSchedule(s, filename)


def demoOptimizeSeats(filename_opponents, filename_seats):
    s = loadSchedule(filename_opponents)
    s.generateSlotsFromGames()

    print("\n*** Loaded schedule")
    Print.printScheduleByGames(s)
    Print.printScheduleByPlayers(s)
    Print.printOpponentsMatrix(s)
    Print.printPairsMatrix(s)

    seats = OptimizeSeats(s, verbose=False)
    seats.optimize(numRuns=10, iterations=[30 * 1000, 30 * 1000])

    print("\n*** Schedule after seats optimization:")
    Print.printScheduleByGames(s)
    Print.printSeatsMatrix(s)

    print("\n*** MWT-compatible schedule")
    Print.printMwtSchedule(s)

    saveSchedule(s, filename_seats)


def demoParticipants(filename_participants):
    numPlayers = 36
    p = Participants.create(numPlayers)
    saveParticipants(p, filename_participants)


def demoMwt(filename, filename_participants):
    s = loadSchedule(filename)

    print("\n*** Loaded schedule")
    Print.printScheduleByGames(s)
    Print.printScheduleByPlayers(s)
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
    if len(sys.argv) < 2:
        print("Expected opponents|seats|show")
        return

    conf = Configurations["VaWaCa-2021"]
    filename_opponents = "vawaca2021_opponents.txt"
    filename_seats = "vawaca2021_seats.txt"
    filename_participants = "participants.txt"

    command = sys.argv[1]
    print(f"Command: {command}")

    if command == "opponents":
        demoOptimizeOpponents(conf, filename_opponents)

    if command == "seats":
        demoOptimizeSeats(filename_opponents, filename_seats)
    
    if command == "participants":
        demoParticipants(filename_participants)

    if command == "show":
        filename = sys.argv[2] if len(sys.argv) >=3 else filename_seats
        demoMwt(filename_seats, filename_participants)
    
if __name__ == '__main__':
    main()
