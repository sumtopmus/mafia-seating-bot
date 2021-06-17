from schedule import *
from metrics import *


class Print:

    @staticmethod
    def printSlots(schedule: Schedule):
        print("\n***Slots:")
        for gameId, slot in schedule.slots.items():
            ids = [player for player in slot.players]
            s = [f"{item:3d}" for item in ids]
            str = ''.join(s)
            print(f"Slot {gameId:2d}: {str}")

    @staticmethod
    def printOpponents(schedule: Schedule):
        m = Metrics(schedule)
        print("\n*** Opponents matrix:")
        for playerId in range(schedule.configuration.numPlayers):
            opponents = m.calcPlayerOpponentsHistogram(playerId)
            s = ''.join([f"{v:3d}" for v in opponents])
            print(f"{playerId:2d}: {s}")

    @staticmethod
    def printGames(schedule: Schedule):
        print("\n***Games:")
        for game in schedule.games:
            ids = [player.id for player in game.players]
            s = [f"{item:3d}" for item in ids]
            str = ''.join(s)
            print(f"Game {game.id:2d}: {str}")

    @staticmethod
    def printSeats(schedule: Schedule):
        m = Metrics(schedule)
        print("\n*** Seats matrix:")
        for playerId in range(schedule.configuration.numPlayers):
            seats = m.calcPlayerSeatsHistogram(playerId)
            s = ''.join([f"{v:3d}" for v in seats])
            print(f"{playerId:2d}: {s}")
