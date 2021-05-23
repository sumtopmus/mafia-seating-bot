from configuration import *

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

    def __init__(self, configuration : Configuration):
        self._configuration = configuration