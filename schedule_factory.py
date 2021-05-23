
from configuration import Configuration
from schedule import *

from player import *
from game import *


class ScheduleFactory:
    def createInitialSchedule(conf : Configuration, participants : Participants):
        playerId = 0

        # create rounds and games
        rounds = []
        games = []
        gameId = 0
        for roundNum in range(conf.NumRounds):
            gamesInRound = []
            
            for tableNum in range(conf.NumTables):
                if len(games) >= conf.NumGames:
                    break

                # prepare players for game
                playerIds = [-1] * 10
                for i in range(10):
                    playerIds[i] = playerId
                    playerId = (playerId + 1) % conf.NumPlayers

                players = []
                for id in playerIds:
                    player = participants.find(id)
                    if not player:
                        raise RuntimeError(f"Player: {id} not found!")
                    players.append(player)

                # create next game
                game = Game(gameId, players)
                gameId = gameId + 1
                games.append(game)
                gamesInRound.append(game)

            # create next round            
            round = Round(roundNum, gamesInRound)
            rounds.append(round)

        schedule = Schedule(conf, participants, rounds, games)
        return schedule