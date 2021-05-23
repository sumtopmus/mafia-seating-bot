class Player:
    '''Single player of torunament. Player has unique <id> and <name>'''

    # id is readonly
    @property
    def id(self):
        return self._id

    # name is read-write
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name
    pass


class Players:
    ''' Players of tournament. Automatically assigns ids to players in constructor'''

    @property
    def players(self):
        return self._players;

    def __init__(self, names : list):
        self._players = []
        
        id : int = 1
        for name in names:
            # create a player
            player = Player(id, name)
            id = id + 1;

            # add player to list
            self._players.append(player)
        pass
