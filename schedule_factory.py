
from configuration import Configuration
from schedule import *

from player import *
from game import *


class ScheduleFactory:
    def createInitialSchedule(conf: Configuration, participants: Participants):
        playerId = 0

        # create rounds and games
        rounds = []
        gameId = 0
        for roundNum in range(conf.numRounds):
            gamesInRound = []

            for tableNum in range(conf.numTables):
                if gameId >= conf.numGames:
                    break

                # prepare players for game
                playerIds = [-1] * 10
                for i in range(10):
                    playerIds[i] = playerId
                    playerId = (playerId + 1) % conf.numPlayers

                players = []
                for id in playerIds:
                    player = participants.find(id)
                    if not player:
                        raise RuntimeError(f'Player: {id} not found!')
                    players.append(player)

                # create next game
                game = Game(gameId, playerIds)
                gameId = gameId + 1
                gamesInRound.append(game)

            # create next round
            round = Round(roundNum, gamesInRound)
            rounds.append(round)

        schedule = Schedule(conf, participants, rounds)
        return schedule
