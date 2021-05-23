from configuration import *

class ScheduleException(Exception):
    pass

class Schedule:
    _configuration : Configuration
    _players = []
    _rounds = []
    _games = []

    @property
    def configuration(self):
        return self._configuration

    @property
    def players(self):
        return self._players

    @property
    def rounds(self):
        return self._rounds

    @property
    def games(self):
        return self._games

    def __init__(self, conf : Configuration = None, players : list = [], rounds : list = [], games : list = []):
        self._configuration = conf
        self._players = players
        self._rounds = rounds
        self._games = games

    def isValid(self) -> bool:
        try:
            self.validate()
        except ScheduleException:
            return False
        return True

    def validate(self) -> bool:
        if len(self._players) != self._configuration.NumPlayers:
            raise ScheduleException(f"Player count: {self._players} must match configuration: {self._configuration.NumPlayers}")
        
        if len(self._rounds) != self._configuration.NumRounds:
            raise ScheduleException(f"Round count: {self._rounds} must match configuration: {self._configuration.NumRounds}")

        if len(self._games) != self._configuration.NumGames:
            raise ScheduleException(f"Game count: {self._games} must match configuration: {self._configuration.NumGames}")

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
            raise ScheduleException(f"All players must play the same number of games")

        # every player must play NumAttempts games
        for player in self._players:
            if player.id not in gamesPlayed:
                raise ScheduleException(f"Player: {player.id} does not play a single game!")

            gamesPlayedById = gamesPlayed[player.id]
            if gamesPlayed[player.id] != self._configuration.NumAttempts:
                raise ScheduleException(f"Player: {player.id} game count: {gamesPlayedById} must match configuration: {self._configuration.NumAttempts}")
