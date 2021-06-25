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

    @staticmethod
    def printPairsMatrix(schedule : Schedule):
        m = Metrics(schedule)

        print("\nPairs matrix:")
        for playerId in range(schedule.numPlayers):
            pairs = m.calcPlayerPairsHistogram(playerId)
            penalty = m.penaltyPlayer(playerId)
            header = f"Player {playerId:2d}: err={penalty:6.2f}: "
            str = ''.join([f"{numPairs:4d}" for numPairs in pairs.values()])
            
            print(f"{header:25s}{str}")

        # ideal line
        hist = m.penaltyIdealHistogram()
        header = f"*** Ideal: "
        str = ''.join([f"{round(numPairs):4d}" for numPairs in hist.values()])
        print(f"{header:25s}{str}")

        # last line
        allPairs = m.calcPairsHistogram()
        header = f"*** Overall: "
        str = ''.join([f"{numPairs:4d}" for numPairs in allPairs.values()])
        print(f"{header:25s}{str}")

    def printMinMaxPairs(schedule : Schedule, numGames: list[int]):
        m = Metrics(schedule)
        
        print("\n*** Min-Max opponents")
        for playerId in range(schedule.numPlayers):         
            pairs = m.calcPlayerPairs(playerId)
            
            header = f"Player {playerId:2d}: "
            str = ""
            for idx in numGames:
                if len(pairs[idx]) == 0:
                    continue
                s = ''.join([f"{id:2d} " for id in pairs[idx]]) if len(pairs[idx]) < 5 else "..."
                str += f"g = {idx} with: [{s}]; "
            print(header, str)


                



        

        

    @staticmethod
    def printPairsHistogram(schedule: Schedule):
        m = Metrics(schedule)
        allPairs = m.calcPairsHistogram()

        print("\nPairs histogram:")
        for numGames, numPairs in allPairs.items():
            if numPairs > 0:
                print(f"{numGames:2d} : {numPairs:3d} pairs")

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
                ids = [schedule.games[gameId].players[seat] for gameId in round.gameIds]

                # output player IDs or player names
                if not schedule.participants:
                    line = [f"{id:>3d}," for id in ids]
                else:
                    line = [f" {schedule.participants.find(id).name}," for id in ids]
                
                # print without last comma
                str = ''.join(line)
                print(str[:-1])
            print()

