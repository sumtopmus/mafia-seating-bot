import json
import math

from .schedule import Schedule
from .player import Player, Participants
from .configuration import Configuration

from .game import Game
from .player import Player
from .round import Round


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


def loadScheduleFromMwt(conf: Configuration, path: str) -> Schedule:

    lines = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # empty game players
    game_players = []
    for game_id in range(conf.numGames):
        empty_list = []
        game_players.append(empty_list)

    # read lines and fill game players list
    idx = 0
    for round_id in range(conf.numRounds):
        start_game_id = round_id * conf.numTables

        # in every round read exactly 10 lines
        for i in range(10):
            line = lines[idx]
            idx += 1

            players = line.split(',')
            for num, player_id in enumerate(players):
                game_id = start_game_id + num
                game_players[game_id].append(int(player_id))

        # after every round there is one empty line
        idx += 1

    games = []
    for game_id in range(conf.numGames):
        game = Game(game_id, game_players[game_id])
        games.append(game)

    round_games = []
    start_game_id = 0
    for round_id in range(conf.numRounds):
        start_game_id = round_id * conf.numTables
        end_game_id = (round_id + 1) * conf.numTables
        # last round may have less than conf.numTables games
        if end_game_id > conf.numGames:
            end_game_id = conf.numGames
        round_games.append(list(range(start_game_id, end_game_id)))

    rounds = []
    for round_id in range(conf.numRounds):
        round = Round(round_id, round_games[round_id])
        rounds.append(round)

    schedule = Schedule(conf, rounds, games)
    return schedule
