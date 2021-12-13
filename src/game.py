import dataclasses

from player import *


# forward declarations
class Game:
    pass

class GameSet:
    pass


@dataclasses.dataclass()
class Game:
    '''
    Game is played by exactly 10 players.
    We store player IDs, not players.
    '''

    id: int
    players: list[int] = dataclasses.field(
        default_factory=list, hash=False, compare=False)

    @staticmethod
    def create(gs: GameSet) -> Game:
        '''Creates a Game from GameSet'''
        players_list = [id for id in gs.players]
        return Game(gs.id, players_list)

    def isValid(self) -> bool:
        # game must have exactly 10 players
        if len(self.players) != 10:
            return False

        # all players must be unique (by id)
        uniquePlayers = set()
        for playerId in self.players:
            if playerId in uniquePlayers:
                return False
            uniquePlayers.add(playerId)
        return True

    @staticmethod
    def fromJson(d: dict):
        players = [playerId for playerId in d['players']]
        return Game(d['id'], players)


class GameSet:
    '''
    Game for opponents optimization, just set of players, without seat numbers
    '''
    
    id: int
    players: set[int] = {}

    def __init__(self, id: int, players: set):
        self.id = id
        self.players = players

    @staticmethod
    def create(game: Game) -> GameSet:
        '''Creates a GameSet from Game'''
        player_set = {id for id in game.players}
        return GameSet(game.id, player_set)


