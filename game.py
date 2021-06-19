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
    '''

    id: int
    players: list[Player] = dataclasses.field(
        default_factory=list, hash=False, compare=False)

    @staticmethod
    def create(gs: GameSet) -> Game:
        '''Creates a Game from GameSet'''
        player_list = [player for player in gs.players]
        return Game(gs.id, player_list)

    def isValid(self) -> bool:
        # game must have exactly 10 players
        if len(self.players) != 10:
            return False

        # all players must be unique (by id)
        uniquePlayers = {}
        for player in self.players:
            if player.id in uniquePlayers:
                return False
            uniquePlayers[player.id] = player.name
        return True

    @staticmethod
    def fromJson(d: dict):
        players = [Player(**item) for item in d['players']]
        return Game(d['id'], players)


class GameSet:
    '''Game for opponents optimization, just set of players, without seat numbers'''
    id: int
    players: set = {}

    def __init__(self, id: int, players: set):
        self.id = id
        self.players = players

    @staticmethod
    def create(game: Game) -> GameSet:
        '''Creates a GameSet from Game'''
        return GameSet(game.id, {player.id for player in game.players})


@dataclasses.dataclass(frozen=True, order=False)
class Round:
    '''
    Round is set of games played at the same time.
    Therefore, any player can be only in one of its games.
    '''
    id: int
    games: list[Game] = dataclasses.field(
        hash=False, compare=False, default_factory=list)

    @staticmethod
    def fromJson(d: dict):
        games = [Game.fromJson(item) for item in d['games']]
        return Round(d['id'], games)
