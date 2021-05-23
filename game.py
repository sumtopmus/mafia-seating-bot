class Game:
    '''
    Game is played by exactly 10 players.
    '''
    @property 
    def id(self):
        return self._id
    
    @property
    def players(self):
        return self._players

    def __init__(self, id : int, players : list):
        self._id = id
        self._players = players

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

class Round:
    '''
    Round is set of games played at the same time.
    Therefore, any player can be only in one of its games.
    '''
    @property
    def id(self):
        return self._id

    @property
    def games(self):
        return self._games

    def __init__(self, id, games):
        self._id = id
        self._games = games

