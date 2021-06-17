import dataclasses


@dataclasses.dataclass(frozen=True)
class Player:
    '''Single player of torunament. Player has unique <id> and <name>'''

    id: int
    name: str
    pass


@dataclasses.dataclass(order=False, )
class Participants:
    ''' Participants of tournament. Automatically assigns ids to players in constructor'''

    people: list[Player] = dataclasses.field(default_factory=list)
    #_peopleDict : dict[int, Player] = field(init = False, repr = False, hash = False, compare = False, default_factory=dict)

    def __len__(self):
        return len(self.people)

    def __getitem__(self, index):
        return self.people[index]

    def find(self, id):
        return self._peopleDict.get(id)

    def __post_init__(self):
        self._peopleDict = {}
        for player in self.people:
            if player.id in self._peopleDict:
                raise RuntimeError(
                    f'Can not create participants: non-unique player id: {player.id}')
            self._peopleDict[player.id] = player

    @staticmethod
    def create(count: int):
        names = Participants.generateNames(count)
        return Participants.createFromNames(names)

    @staticmethod
    def createFromNames(names: list):
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
        s = prefix if prefix is not None else 'Player_'

        names = []
        for id in range(count):
            name = f"{s}{id}"
            names.append(name)
        return names

    @staticmethod
    def fromJson(d: dict):
        p = [Player(**p) for p in d['people']]
        return Participants(p)

    pass