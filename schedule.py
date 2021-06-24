import dataclasses

from configuration import *
from player import *
from game import *


class ScheduleException(Exception):
    pass


class Schedule:
    _configuration: Configuration
    _participants: Participants
    _rounds = []
    _games = []

    @property
    def configuration(self):
        return self._configuration

    @property
    def participants(self):
        return self._participants

    @property
    def rounds(self):
        return self._rounds

    @property
    def games(self):
        return self._games

    @property
    def numPlayers(self):
        return self._configuration.numPlayers

    @property
    def numTables(self):
        return self._configuration.numTables

    @property
    def numRounds(self):
        return self._configuration.numRounds

    @property
    def numGames(self):
        return self._configuration.numGames

    @property
    def numAttempts(self):
        return self._configuration.numAttempts

    def __init__(self, conf: Configuration = None, participants: Participants = None, rounds: list = [], games: list = []):
        self._configuration = conf
        self._participants = participants
        self._rounds = rounds
        self._games = games

    # TODO: make shallow copy, deep copy of Schedule
    #__copy__(), __deepcopy__()

    def toJson(self):
        d = {}
        d['configuration'] = dataclasses.asdict(self._configuration)
        d['participants'] = dataclasses.asdict(self._participants)
        d['rounds'] = [dataclasses.asdict(round) for round in self._rounds]
        d['games'] = [dataclasses.asdict(game) for game in self._games]
        return d

    @staticmethod
    def fromJson(d: dict):
        conf = Configuration(**d['configuration'])
        participants = Participants.fromJson(d['participants'])
        rounds = [Round.fromJson(item) for item in d['rounds']]
        games = [Game.fromJson(item) for item in d['games']]
        return Schedule(conf, participants, rounds, games)

    def generateSlotsFromGames(self):
        self.slots = {}
        for game in self.games:
            self.slots[game.id] = GameSet.create(game)

    def updateGamesFromSlots(self):
        for id in range(len(self.slots)):
            slot = self.slots[id]
            game = self.games[id]
            for i, playerId in enumerate(slot.players):
                game.players[i] = playerId
        # Careful. Now we have both games and slots and they may not match each other...
        # self.slots = {}

    def isValid(self) -> bool:
        try:
            self.validate()
        except ScheduleException:
            return False
        return True

    def validate(self) -> bool:
        if len(self._participants) != self.numPlayers:
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
            lastRoundGames = self.numGames - (self.numRounds - 1) * self.numTables
            if i < len(self.rounds) - 1:
                if len(round.gameIds) != fullRoundGames:
                    raise ScheduleException(f"Wrong game count in round: {i}. Expected: {fullRoundGames}, got: {len(round.gameIds)}")
            else:
                if len(round.gameIds) != lastRoundGames:
                    raise ScheduleException(f"Wrong game count in last round: {id}. Expected: {lastRoundGames}, got: {len(round.gameIds)}")

        # check that rounds have all games in games
        # check every game is in one and only one round
        allIds = {game.id for game in self._games}
        leftIds = allIds.copy()
        for round in self._rounds:
            for gameId in round.gameIds:
                if gameId not in allIds:
                    raise ScheduleException(f"Wrong game id: {gameId} in round: {round.id}")
                if gameId not in leftIds:
                    raise ScheduleException(f"Duplicate game id: {gameId} in round: {round.id}")
                else:
                    leftIds.remove(gameId)
        if len(leftIds) != 0:
            raise ScheduleException(f"Some games are not in any round: {leftIds}")

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
        for player in self._participants:
            if player.id not in gamesPlayed:
                raise ScheduleException(
                    f"Player: {player.id} does not play a single game!")

            gamesPlayedById = gamesPlayed[player.id]
            if gamesPlayed[player.id] != self._configuration.numAttempts:
                raise ScheduleException(
                    f"Player: {player.id} game count: {gamesPlayedById} must match configuration: {self._configuration.numAttempts}")
