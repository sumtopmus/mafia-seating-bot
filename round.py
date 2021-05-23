class Round:
    '''
    Round is set of games played at the same time.
    Therefore, any player can be only in one of its games.
    '''

    _games = []

    @property
    def games(self):
        return self._games

    def __init__(self, games):
        self._games = games