from game import *
from player import *
from schedule import Schedule


class Metrics:
    def __init__(self, schedule: Schedule):
        self.schedule = schedule

    def calcPlayerOpponentsHistogram(self, thisPlayerId: int):
        # initialize opponents histogram
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
        # initialize seats histogram
        seats = [0] * 10

        # go through all games
        for game in self.schedule.games:
            for seat_idx in range(0, 10):
                if game.players[seat_idx].id == thisPlayerId:
                    seats[seat_idx] += 1
        return seats

    def calcSquareDeviationExclude(self, data: list, target: float, exclude_idx: int):
        sd = -(data[exclude_idx] - target) * (data[exclude_idx] - target)
        for i in range(len(data)):
            sd += (data[i] - target) * (data[i] - target)

        return sd / (len(data) - 1)

    def calcSquareDeviation(self, data: list, target: float):
        sd = 0.0
        for i in range(len(data)):
            sd += (data[i] - target) * (data[i] - target)

        return sd / len(data)

    pass
