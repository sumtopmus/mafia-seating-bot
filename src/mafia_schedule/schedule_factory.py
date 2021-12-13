
from configuration import Configuration
from schedule import *
from round import *
from game import *
from player import *

class ScheduleFactory:
    def createInitialSchedule(conf: Configuration):
        if not conf.isValid():
            return None

        # create rounds and games
        rounds = []
        games = []
        gameId = 0
        playerId = 0
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

                # create next game
                game = Game(gameId, playerIds)
                games.append(game)
                gamesInRound.append(gameId)
                gameId = gameId + 1                

            # create next round
            round = Round(roundNum, gamesInRound)
            rounds.append(round)

        schedule = Schedule(conf, rounds, games)
        return schedule
