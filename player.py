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

    def toJson(self) -> dict:
        return {"id": self._id, "name": self._name}

    @staticmethod
    def fromJson(d: dict):
        return Player(d["id"], d["name"])
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

    def __init__(self, people: list):
        self._all = []
        self._dict = {}

        for player in people:
            self._all.append(player)
            if player.id in self._dict:
                raise RuntimeError(f"Can not create participants: non-unique player id: {player.id}")
            self._dict[player.id] = player

    @staticmethod
    def create(count:int):
        names = Participants.generateNames(count)
        return Participants.createFromNames(names)

    @staticmethod
    def createFromNames(names:list):
        people = []
        id = 0
        for name in names:
            # create a player and add to dict
            player = Player(id, name)
            id = id + 1
            people.append(player)
            
        return Participants(people)

    @staticmethod
    def generateNames(count: int, prefix: str = None):
        s = prefix if prefix is not None else "Player_"

        names = []
        for id in range(count):
            name = f"{s}{id}"
            names.append(name)
        return names

    def toJson(self) -> dict:
        return {"people": [player.toJson() for player in self._all if player]}

    @staticmethod
    def fromJson(d: dict):
        return Participants([Player.fromJson(p) for p in d["people"] if True])

    pass
