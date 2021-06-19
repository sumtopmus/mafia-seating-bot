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
    def numAttempts(self):
        return self._configuration.numAttempts

    def __init__(self, conf: Configuration = None, participants: Participants = None, rounds: list = [], games: list = []):
        self._configuration = conf
        self._participants = participants
        self._rounds = rounds

        # reconstruct plain games list from rounds
        self._games = []
        for round in self._rounds:
            self._games.extend(round.games)

    # TODO: make shallow copy, deep copy of Schedule
    #__copy__(), __deepcopy__()

    def toJson(self):
        d = {}
        d['configuration'] = dataclasses.asdict(self._configuration)
        d['participants'] = dataclasses.asdict(self._participants)
        d['rounds'] = [dataclasses.asdict(round) for round in self._rounds]
        # we actually don't need to serialize games, they are in rounds...
        return d

    @staticmethod
    def fromJson(d: dict):
        conf = Configuration.fromJson(d['configuration'])
        participants = Participants.fromJson(d['participants'])
        rounds = [Round.fromJson(d) for d in d['rounds']]
        return Schedule(conf, participants, rounds)

    def generateSlotsFromGames(self):
        self.slots = {}
        for game in self.games:
            self.slots[game.id] = GameSet.create(game)

    def updateGamesfromSlots(self):
        for id in range(len(self.slots)):
            slot = self.slots[id]
            game = self.games[id]
            for i, playerId in enumerate(slot.players):
                game.players[i] = self.participants.find(playerId)
        # Careful. Now we have both games and slots and they may not match each other...
        # self.slots = {}

    def isValid(self) -> bool:
        try:
            self.validate()
        except ScheduleException:
            return False
        return True

    def validate(self) -> bool:
        if len(self._participants) != self._configuration.numPlayers:
            raise ScheduleException(
                f"Participant count: {self._players} must match configuration: {self._configuration.numPlayers}")

        if len(self._rounds) != self._configuration.numRounds:
            raise ScheduleException(
                f"Round count: {self._rounds} must match configuration: {self._configuration.numRounds}")

        if len(self._games) != self._configuration.numGames:
            raise ScheduleException(
                f"Game count: {self._games} must match configuration: {self._configuration.numGames}")

        # calc number of games played by every player
        gamesPlayed = {}
        for game in self._games:
            for player in game.players:
                gamesPlayedById = 1 + gamesPlayed.get(player.id, 0)
                gamesPlayed[player.id] = gamesPlayedById

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
