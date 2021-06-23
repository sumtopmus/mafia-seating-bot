from schedule import *
from schedule_factory import *

from player import *
from game import *
from metrics import *
from print import *

from optimize_opponents import *
from optimize_seats import *

import json
import os.path


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


def saveSchedule(schedule: Schedule, fname: str):
    jsonDict = schedule.toJson()
    jsonStr = json.dumps(jsonDict, indent=2)

    home = os.path.expanduser("~")
    filename = os.path.join(home, fname)
    print(f"Saving schedule to: {filename}")
    with open(filename, "w") as f:
        f.write(jsonStr)


def loadSchedule(fname: str) -> Schedule:
    home = os.path.expanduser("~")
    filename = os.path.join(home, fname)
    print(f"Loading schedule from: {filename}")
    with open(filename, "r") as f:
        s = f.read()
    d = json.loads(s)

    s = Schedule.fromJson(d)
    s.generateSlotsFromGames()
    return s


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


def demoOpponents():
    conf = Configurations["GG-2021"]
    participants = Participants.create(conf.numPlayers)

    opponents = OptimizeOpponents(verbose=False)
    s = opponents.optimize(conf, participants, stages=5, iterations=25 * 1000)

    print("\n*** Schedule after opponents optimization:")
    Print.printScheduleByGames(s)
    Print.printOpponentsMatrix(s)
    Print.printPairsHistogram(s)

    Print.printMwtSchedule(s)
    saveSchedule(s, "schedule_opponents.txt")


def demoSeats():
    s = loadSchedule("schedule_opponents.txt")
    s.generateSlotsFromGames()

    Print.printMwtSchedule(s)

    print("\n*** Initial schedule")
    Print.printScheduleByGames(s)
    Print.printPairsHistogram(s)

    seats = OptimizeSeats(s, verbose=False)
    seats.optimize(iterations=[20 * 1000, 50 * 1000])

    print("\n*** Schedule after seats optimization:")
    Print.printScheduleByGames(s)

    # sanity check
    Print.printPairsHistogram(s)
    Print.printSeatsMatrix(s)

    Print.printMwtSchedule(s)
    saveSchedule(s, "schedule_seats.txt")


# demoOpponents()
demoSeats()
