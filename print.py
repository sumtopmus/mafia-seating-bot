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
    def printOpponentsMatrix(schedule: Schedule):
        m = Metrics(schedule)
        matrix = m.calcOpponentsMatrix()

        print("\n*** Opponents matrix:")
        for playerId in range(len(matrix)):
            line = matrix[playerId]
            s = ''.join([f"{v:3d}" for v in line])
            print(f"{playerId:2d}: {s}")

    def printPairsHistogram(schedule: Schedule):
        m = Metrics(schedule)
        matrix = m.calcOpponentsMatrix()

        pairs = {}
        for val in range(schedule.numAttempts + 1):
            pairs[val] = 0

        for playerId in range(len(matrix)):
            line = matrix[playerId]
            for opponentId in range(playerId):
                numGames = line[opponentId]
                pairs[numGames] += 1

        print("\nPairs histogram:")
        for numGames, count in pairs.items():
            if count > 0:
                print(f"{numGames:2d} : {count:3d} pairs")

    @staticmethod
    def printScheduleByGames(schedule: Schedule):
        print("\nSchedule by games:")
        for round in schedule.rounds:
            print(f"\nRound: {round.id + 1}")
            for gameId in round.gameIds:
                game = schedule.games[gameId]
                s = [f"{id:3d}" for id in game.players]
                str = ''.join(s)
                print(f"Game {game.id:2d}: {str}")

    @staticmethod
    def printSeatsMatrix(schedule: Schedule):
        m = Metrics(schedule)

        matrix = m.calcSeatsMatrix()
        print("\n*** Seats matrix:")
        for playerId in range(len(matrix)):
            line = matrix[playerId]
            s = ''.join([f"{v:3d}" for v in line])
            print(f"{playerId:2d}: {s}")

    @staticmethod
    def printMwtSchedule(schedule : Schedule):
        for round in schedule.rounds:
            for seat in range(10):
                line = [f"{schedule.games[gameId].players[seat]:3d}," for gameId in round.gameIds]
                str = ''.join(line)
                # print without last comma
                print(str[:-1])
            print()

