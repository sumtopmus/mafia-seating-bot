from game import *
from player import *
from schedule import Schedule


class Metrics:
    def __init__(self, schedule: Schedule):
        self.schedule = schedule

    def calcPlayerOpponentsHistogram(self, thisPlayerId: int):
        '''
        Calculates opponents histogram for given <thisPlayerId>
        Returns a list of size <numPlayers>,
        where value of a[i] - total number of games that pair of players <thisPlayerId>, <i> are playing
        '''
        opponents = [0] * self.schedule.numPlayers

        # go through all games
        for game in self.schedule.games:
            slot = self.schedule.slots[game.id]
            if thisPlayerId in slot.players:
                for player in game.players:
                    if thisPlayerId != player.id:
                        opponents[player.id] += 1

        return opponents

    def calcPlayerSeatsHistogram(self, thisPlayerId: int):
        '''
        Calculates seats histogram for given <thisPlayerId>
        Returns a list of size 10,
        where value of a[i] - total numbe of games where player sits on seat number <i>
        '''
        seats = [0] * 10

        # go through all games
        for game in self.schedule.games:
            for seat_idx in range(0, 10):
                if game.players[seat_idx].id == thisPlayerId:
                    seats[seat_idx] += 1
        return seats

    def calcSquareDeviationExclude(self, data: list, target: float, exclude_idx: int):
        '''
        Calculates standard deviation between values in <data> and <target>, 
        except for item data[exclude_idx].
        '''
        sd = -(data[exclude_idx] - target) * (data[exclude_idx] - target)
        for i in range(len(data)):
            sd += (data[i] - target) * (data[i] - target)
        return sd / (len(data) - 1)

    def calcSquareDeviation(self, data: list, target: float):
        '''
        Calculates standard deviation between values in <data> and <target> value.
        '''
        sd = 0.0
        for i in range(len(data)):
            sd += (data[i] - target) * (data[i] - target)
        return sd / len(data)

    pass
