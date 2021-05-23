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


class Participants:
    ''' Participants of tournament. Automatically assigns ids to players in constructor'''

    @property
    def all(self):
        return self._all

    def __len__(self):
        return len(self._all)

    def __getitem__(self, index):
        return self._all[index]

    def find(self, id):
        return self._dict.get(id)
    
    def __init__(self, names : list): 
        self._all = []
        self._dict = {}       
        
        id = 0
        for name in names:
            # create a player and add to dict
            player = Player(id, name)
            self._all.append(player)
            self._dict[id] = player
            id = id + 1
    
    @staticmethod
    def generateNames(count : int, prefix : str = None):
        s = prefix if prefix is not None else "Player_"

        names = []
        for id in range(count):
            name = f"{s}{id+1}"
            names.append(name)
        return names

    pass
