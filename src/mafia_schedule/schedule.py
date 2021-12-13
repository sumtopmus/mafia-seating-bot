import dataclasses

from .configuration import *
from .round import *
from .game import *
from .player import *


class ScheduleException(Exception):
    pass


class Schedule:
    _configuration: Configuration
    _participants: Participants
    _rounds = list[Round]
    _games = list[Game]

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    @property
    def participants(self) -> Participants:
        return self._participants

    @property
    def rounds(self) -> list[Round]:
        return self._rounds

    @property
    def games(self) -> list[Game]:
        return self._games

    @property
    def numPlayers(self) -> int:
        return self._configuration.numPlayers

    @property
    def numTables(self) -> int:
        return self._configuration.numTables

    @property
    def numRounds(self) -> int:
        return self._configuration.numRounds

    @property
    def numGames(self) -> int:
        return self._configuration.numGames

    @property
    def numAttempts(self) -> int:
        return self._configuration.numAttempts

    def __init__(self, conf: Configuration = None, rounds: list = [], games: list = []):
        self._configuration = conf
        self._participants = None
        self._rounds = rounds
        self._games = games

    def setParticipants(self, people: Participants):
        self._participants = people

    def toJson(self):
        d = {}
        d['configuration'] = dataclasses.asdict(self._configuration)
        d['rounds'] = [dataclasses.asdict(round) for round in self._rounds]
        d['games'] = [dataclasses.asdict(game) for game in self._games]
        return d

    @staticmethod
    def fromJson(d: dict):
        conf = Configuration(**d['configuration'])
        rounds = [Round.fromJson(item) for item in d['rounds']]
        games = [Game.fromJson(item) for item in d['games']]
        return Schedule(conf, rounds, games)

    def generateSlotsFromGames(self):
        self.slots = {}
        for game in self.games:
            self.slots[game.id] = GameSet.create(game)

    def updateGamesFromSlots(self):
        for slotId in self.slots:
            self.games[slotId] = Game.create(self.slots[slotId])
        # Careful. Now we have both games and slots and they may not match each other...
        # self.slots = {}

    def saveGamePlayers(self) -> dict[int, list[int]]:
        '''
        Saves players of all games to dictionary.
        This function is used by multi-run seats optimization.
        '''
        gamePlayers = {}
        for game in self.games:
            gamePlayers[game.id] = list(game.players)
        return gamePlayers

    def updateGamePlayers(self, gamePlayers: dict[int, list[int]]):
        '''
        Loads game players from external dictionary.
        This function is used by multi-run seats optimization.
        '''
        for game in self.games:
            if game.id not in gamePlayers.keys():
                raise RuntimeError(
                    f"UpdatePlayers. Game: {game.id} is not specified in gamePlayers!")
            players = gamePlayers[game.id]
            game.players = list(players)

    def isValid(self) -> bool:
        try:
            self.validate()
        except ScheduleException:
            return False
        return True

    def validateGame(self, game):
        players = set[int]()
        for playerId in game.players:
            if playerId < 0 or playerId > self.numPlayers:
                raise ScheduleException(f"Invalid player id: {player.id}")
            if playerId in players:
                raise ScheduleException(
                    f"Player: {playerId} can not play in a single game #{game.id} twice!")
            players.add(playerId)

    def validateRound(self, round):
        players = set[int]()
        for gameId in round.gameIds:
            game = self.games[gameId]
            for playerId in game.players:
                if playerId in players:
                    raise ScheduleException(
                        f"Player: {playerId} can not play in a single round #{round.id} twice!")
                players.add(playerId)

    def validate(self):
        if self._participants != None and len(self._participants) != self.numPlayers:
            raise ScheduleException(
                f"Participant count: {self._players} must match configuration: {self.numPlayers}")

        if len(self._rounds) != self.numRounds:
            raise ScheduleException(
                f"Round count: {self._rounds} must match configuration: {self.numRounds}")

        if len(self._games) != self.numGames:
            raise ScheduleException(
                f"Game count: {self._games} must match configuration: {self.numGames}")

        # check game count in rounds
        for i, round in enumerate(self._rounds):
            fullRoundGames = self.numTables
            lastRoundGames = self.numGames - \
                (self.numRounds - 1) * self.numTables
            if i < len(self.rounds) - 1:
                if len(round.gameIds) != fullRoundGames:
                    raise ScheduleException(
                        f"Wrong game count in round: {i}. Expected: {fullRoundGames}, got: {len(round.gameIds)}")
            else:
                if len(round.gameIds) != lastRoundGames:
                    raise ScheduleException(
                        f"Wrong game count in last round: {id}. Expected: {lastRoundGames}, got: {len(round.gameIds)}")

        # check that rounds have all games in games
        # check every game is in one and only one round
        allIds = {game.id for game in self._games}
        leftIds = allIds.copy()
        for round in self._rounds:
            for gameId in round.gameIds:
                if gameId not in allIds:
                    raise ScheduleException(
                        f"Wrong game id: {gameId} in round: {round.id}")
                if gameId not in leftIds:
                    raise ScheduleException(
                        f"Duplicate game id: {gameId} in round: {round.id}")
                else:
                    leftIds.remove(gameId)
        if len(leftIds) != 0:
            raise ScheduleException(
                f"Some games are not in any round: {leftIds}")

        # validate game
        for game in self._games:
            self.validateGame(game)

        # validate round
        for round in self._rounds:
            self.validateRound(round)

        # calc number of games played by every player
        gamesPlayed = {}
        for game in self._games:
            for playerId in game.players:
                num = 1 + gamesPlayed.get(playerId, 0)
                gamesPlayed[playerId] = num

        # all players must play the same number of attempts
        counts = gamesPlayed.values()
        gamesPlayedSet = set(counts)
        if len(gamesPlayedSet) != 1:
            raise ScheduleException(
                f"All players must play the same number of games")

        # every player must play NumAttempts games
        for playerId in range(self.numPlayers):
            if playerId not in gamesPlayed:
                raise ScheduleException(
                    f"Player: {playerId} does not play a single game!")

            gamesPlayedById = gamesPlayed[playerId]
            if gamesPlayed[playerId] != self.numAttempts:
                raise ScheduleException(
                    f"Player: {player.id} game count: {gamesPlayedById} must match configuration: {self.numAttempts}")
