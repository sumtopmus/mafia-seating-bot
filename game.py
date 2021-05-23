class Game:
    '''
    Game is played by exactly 10 players.
    '''

    _players = []
    @property
    def players(self):
        return self._players

    def __init__(self, players):
        self._players = players;

    def isValid(self) -> bool:
        # game must have exactly 10 players
        if len(self._players) != 10:
            return False
        
        # all players must be unique (by id)
        uniquePlayers = {}
        for player in self._players:
            if player.id in uniquePlayers:
                return False
            uniquePlayers[player.id] = player.name
        return True

