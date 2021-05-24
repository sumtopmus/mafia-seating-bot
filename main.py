from schedule import *
from schedule_factory import *

from player import *
from game import *
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

    conf = Configuration(numPlayers, numTables = 1, numRounds = 1, numGames = 1, numAttempts = 1)
    schedule = ScheduleFactory.createInitialSchedule(conf, participants)
    d = schedule.toJson()
    print(f"Schedule:\n{json.dumps(d, indent=2)}")


# serializeDictionaryDemo()
# serializePlayerDemo()
serializeScheduleDemo()


