import json
import os.path

from .schedule import Schedule
from .player import Player, Participants


def saveSchedule(schedule: Schedule, path: str):
    jsonDict = schedule.toJson()
    jsonStr = json.dumps(jsonDict, indent=2)

    print(f"Saving schedule to: {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(jsonStr)


def saveParticipants(participants: Participants, path: str):
    jsonDict = participants.toJson()
    jsonStr = json.dumps(jsonDict, indent=2)

    print(f"Saving participants to: {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(jsonStr)


def loadSchedule(path: str) -> Schedule:
    print(f"Loading schedule from: {path}")
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    d = json.loads(s)

    s = Schedule.fromJson(d)
    s.generateSlotsFromGames()
    return s


def loadParticipants(path: str) -> Participants:
    print(f"Loading participants from: {path}")
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    d = json.loads(s)

    participants = Participants.fromJson(d)
    return participants
