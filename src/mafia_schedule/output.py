from typing import Callable

from .schedule import Schedule
from .metrics import Metrics


class Print:
    @staticmethod
    def print(func: Callable):
        for line in func:
            print(line)

    @staticmethod
    def slots(schedule: Schedule):
        yield ''
        yield "*** Slots:"
        for gameId, slot in schedule.slots.items():
            ids = [player for player in slot.players]
            s = [f"{item:3d}" for item in ids]
            str = ''.join(s)
            yield f"Slot {gameId:2d}: {str}"

    @staticmethod
    def opponentsMatrix(schedule: Schedule):
        m = Metrics(schedule)
        matrix = m.calcOpponentsMatrix()

        yield ''
        yield "*** Opponents matrix:"
        for playerId in range(len(matrix)):
            line = matrix[playerId]
            s = ''.join([f"{v:3d}" for v in line])
            yield f"{playerId:2d}: {s}"

    @staticmethod
    def pairsMatrix(schedule: Schedule):
        m = Metrics(schedule)

        yield ''
        yield "Pairs matrix:"
        for playerId in range(schedule.numPlayers):
            pairs = m.calcPlayerPairsHistogram(playerId)
            penalty = m.penaltyPlayer(playerId)
            header = f"Player {playerId:2d}: err={penalty:6.2f}: "
            str = ''.join([f"{numPairs:4d}" for numPairs in pairs.values()])

            yield f"{header:25s}{str}"

        # ideal line
        hist = m.penaltyIdealHistogram()
        header = f"*** Ideal: "
        str = ''.join([f"{round(numPairs):4d}" for numPairs in hist.values()])
        yield f"{header:25s}{str}"

        # last line
        allPairs = m.calcPairsHistogram()
        header = f"*** Overall: "
        str = ''.join([f"{numPairs:4d}" for numPairs in allPairs.values()])
        yield f"{header:25s}{str}"

    def minMaxPairs(schedule: Schedule, numGames: list[int]):
        m = Metrics(schedule)

        yield ''
        yield "*** Min-Max opponents:"
        for playerId in range(schedule.numPlayers):
            pairs = m.calcPlayerPairs(playerId)

            header = f"Player {playerId:2d}: "
            str = ""
            for idx in numGames:
                if len(pairs[idx]) == 0:
                    continue
                s = ''.join([f"{id:2d} " for id in pairs[idx]]
                            ) if len(pairs[idx]) < 5 else "..."
                str += f"g = {idx} with: [{s}]; "
            yield f"{header}{str}"

    @staticmethod
    def pairsHistogram(schedule: Schedule):
        m = Metrics(schedule)
        allPairs = m.calcPairsHistogram()

        yield ''
        yield "Pairs histogram:"
        for numGames, numPairs in allPairs.items():
            if numPairs > 0:
                yield f"{numGames:2d} : {numPairs:3d} pairs"

    @staticmethod
    def scheduleByGames(schedule: Schedule):
        yield ''
        yield "Schedule by games:"
        for round in schedule.rounds:
            yield f"\nRound: {round.id}"
            for gameId in round.gameIds:
                game = schedule.games[gameId]
                s = [f"{id:3d}" for id in game.players]
                str = ''.join(s)
                yield f"Game {game.id:2d}: {str}"

    @staticmethod
    def scheduleByPlayers(schedule: Schedule):
        yield ''
        yield "Schedule by players:"
        for playerId in range(schedule.numPlayers):
            str = ""
            for round in schedule.rounds:
                roundStr = f"{' *:* '}"
                for table, gameId in enumerate(round.gameIds):
                    game = schedule.games[gameId]
                    tableStr = chr(ord('A') + table)
                    for seat, id in enumerate(game.players):
                        if id == playerId:
                            roundStr = f" {tableStr}:{(seat+1):<2d}"
                            break
                str += roundStr

            if schedule.participants is None:
                header = f"Player {playerId:2d}: "
            else:
                playerName = schedule.participants[playerId].name
                header = f"{playerName:20}:"
            yield f"{header}{str}"

    @staticmethod
    def seatsMatrix(schedule: Schedule):
        m = Metrics(schedule)
        matrix = m.calcSeatsMatrix()

        yield ''
        yield "*** Seats matrix:"
        for playerId in range(len(matrix)):
            line = matrix[playerId]
            s = ''.join([f"{v:3d}" for v in line])
            yield f"{playerId:2d}: {s}"

    @staticmethod
    def mwtSchedule(schedule: Schedule):
        for round in schedule.rounds:
            for seat in range(10):
                ids = [schedule.games[gameId].players[seat]
                       for gameId in round.gameIds]

                # output player IDs or player names
                if not schedule.participants:
                    line = [f"{id:>3d}," for id in ids]
                else:
                    line = [
                        f" {schedule.participants.find(id).name}," for id in ids]

                # print without last comma
                str = ''.join(line)
                yield str[:-1]
            yield ''
