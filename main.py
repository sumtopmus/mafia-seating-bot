from schedule import *
from schedule_factory import *

from player import *
from game import *
from metrics import *
from print import *

from optimize_opponents import *
from optimize_seats import *

import json


def serializeDictionaryDemo():
    d = {"a": 1, "b": 2}
    s = json.dumps(d)
    print(f"Serialized dictionary:\n{s}")


def serializePlayerDemo():
    print("Create a player")
    player = Player(1, "like")

    playerDict = player.toJson()
    print(f"Original player:\n{json.dumps(playerDict)}")

    print("Restore player from JSON dict")
    playerRestored = Player.fromJson(playerDict)

    playerRestoredDict = playerRestored.toJson()
    print(f"Restored player:\n{json.dumps(playerRestoredDict)}")


def serializeScheduleDemo():
    numPlayers = 10
    participants = Participants.create(numPlayers)

    conf = Configuration(numPlayers, numTables=1,
                         numRounds=1, numGames=1, numAttempts=1)
    schedule = ScheduleFactory.createInitialSchedule(conf, participants)
    d = schedule.toJson()
    print(f"Schedule:\n{json.dumps(d, indent=2)}")


def demoInitialSchedule():
    numPlayers = 12
    participants = Participants.create(numPlayers)

    conf = Configuration(numPlayers, numTables=1,
                         numRounds=6, numGames=6, numAttempts=5)
    s = ScheduleFactory.createInitialSchedule(conf, participants)

    s.generateSlotsFromGames()

    Print.printSlots(s)
    Print.printOpponents(s)
    Print.printSeats(s)


def scheduleVaWaCa2017():
    numPlayers = 25
    participants = Participants.create(numPlayers)

    conf = Configuration(numPlayers, numTables=2,
                         numRounds=10, numGames=20, numAttempts=8)
    return ScheduleFactory.createInitialSchedule(conf, participants)


def scheduleWaCa2019():
    numPlayers = 30
    participants = Participants.create(numPlayers)

    conf = Configuration(numPlayers, numTables=3,
                         numRounds=10, numGames=30, numAttempts=10)
    return ScheduleFactory.createInitialSchedule(conf, participants)


def scheduleMini():
    numPlayers = 13
    participants = Participants.create(numPlayers)
    conf = Configuration(numPlayers, numTables=1,
                         numRounds=13, numGames=13, numAttempts=10)
    return ScheduleFactory.createInitialSchedule(conf, participants)


def scheduleGoldenGate2021():
    numPlayers = 36
    participants = Participants.create(numPlayers)
    conf = Configuration(numPlayers, numTables=3,
                         numRounds=12, numGames=36, numAttempts=10)
    return ScheduleFactory.createInitialSchedule(conf, participants)


'''
def demoOptimizeOpponents(s : Schedule):
    s.generateSlotsFromGames()

    print("Initial schedule")
    Print.printSlots(s)
    Print.printOpponents(s)
    Print.printSeats(s)

    solve = OptimizeOpponents(s)
    solve.optimize(maxIterations=1000)

    print("Final schedule")
    Print.printSlots(s)
    Print.printOpponents(s)
    Print.printSeats(s)

    print("Final games:")
    s.updateGamesfromSlots()
    Print.printGames(s)
'''

'''
def demoOptimizeSeats(s : Schedule):
    s = scheduleWaCa2019()

    print("Initial SEAT schedule")
    Print.printGames(s)
    Print.printSeats(s)   

    solve = OptimizeSeats(s)
    solve.optimize(maxIterations=1000)

    print("Final SEAT schedule")
    Print.printGames(s)
    # Print.printOpponents(s)
    Print.printSeats(s)
'''


def demoOptimize(s: Schedule):
    s.generateSlotsFromGames()

    print("\n*** Initial schedule")
    Print.printScheduleByGames(s)
    Print.printPairsHistogram(s)

    solve = OptimizeOpponents(s, verbose = False)
    solve.optimize(stages=5, iterations=10 * 1000)

    print("\n*** Schedule after opponents optimization:")
    Print.printScheduleByGames(s)
    Print.printOpponentsMatrix(s)
    Print.printPairsHistogram(s)

# serializeDictionaryDemo()
# serializePlayerDemo()
# serializeScheduleDemo()

# demoInitialSchedule()


'''s = scheduleMini() 
demoOptimizeOpponents(s)
demoOptimizeSeats(s)'''

s = scheduleGoldenGate2021()
demoOptimize(s)
