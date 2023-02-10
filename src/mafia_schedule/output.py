from collections import defaultdict
from typing import Callable

from .format import Format
from .schedule import Schedule
from .round import Round
from .metrics import Metrics


class Print:
    @staticmethod
    def print(func: Callable):
        for line in func:
            print(line)

    @ staticmethod
    def slots(schedule: Schedule):
        yield ''
        yield "*** Slots:"
        for gameId, slot in schedule.slots.items():
            ids = [player for player in slot.players]
            s = [f"{item:3d}" for item in ids]
            str = ''.join(s)
            yield f"Slot {gameId:2d}: {str}"

    @ staticmethod
    def opponentsMatrix(schedule: Schedule):
        f = Format(schedule)
        m = Metrics(schedule)
        matrix = m.calcOpponentsMatrix()

        yield ''
        yield "*** Opponents matrix:"
        for playerId in range(len(matrix)):
            line = matrix[playerId]
            s = ''.join([f"{v:3d}" for v in line])
            yield f"{f.pretty_player_id(playerId):<20}: {s}"

    @ staticmethod
    def pairsMatrix(schedule: Schedule):
        f = Format(schedule)
        m = Metrics(schedule)

        yield ''
        yield "Pairs matrix:"
        for playerId in range(schedule.numPlayers):
            pairs = m.calcPlayerPairsHistogram(playerId)
            penalty = m.penaltyPlayer(playerId)
            header = f"{f.pretty_player_id(playerId):<20}: err={penalty:6.2f}: "
            str = ''.join([f"{numPairs:4d}" for numPairs in pairs.values()])

            yield f"{header: <35s}{str}"

        # ideal line
        hist = m.penaltyIdealHistogram()
        header = f"*** Ideal: "
        str = ''.join([f"{round(numPairs):4d}" for numPairs in hist.values()])
        yield f"{header: <35s}{str}"

        # last line
        allPairs = m.calcPairsHistogram()
        header = f"*** Overall: "
        str = ''.join([f"{numPairs:4d}" for numPairs in allPairs.values()])
        yield f"{header: <35s}{str}"

    def minMaxPairs(schedule: Schedule, numGames: list[int]):
        f = Format(schedule)
        m = Metrics(schedule)

        yield ''
        yield f"*** Min-Max opponents: {numGames}"
        for playerId in range(schedule.numPlayers):
            pairs = m.calcPlayerPairs(playerId)

            header = f"{f.pretty_player_id(playerId):<2}: "
            str = ""
            for idx in numGames:
                if idx >= len(pairs) or len(pairs[idx]) == 0:
                    continue
                s = ''.join([f"{f.pretty_player_id(id):<2} " for id in pairs[idx]]
                            ) if len(pairs[idx]) < 5 else "..."
                element = f"g = {idx} with: [{s}]; " if len(
                    numGames) > 1 else f"with: [{s}]"
                str += element
            yield f"{header}{str}"

    @ staticmethod
    def pairsHistogram(schedule: Schedule):
        m = Metrics(schedule)
        allPairs = m.calcPairsHistogram()

        yield ''
        yield "Pairs histogram:"
        for numGames, numPairs in allPairs.items():
            if numPairs > 0:
                yield f"{numGames:2d} : {numPairs:3d} pairs"

    @ staticmethod
    def scheduleByGames(schedule: Schedule):
        f = Format(schedule)
        yield ''
        yield "Schedule by games:"
        for round in schedule.rounds:
            yield f"\nRound: {f.pretty_round_id(round.id)}"
            for table_id, game_id in enumerate(round.gameIds):
                game = schedule.games[game_id]

                # with seat num
                # s = [
                #    f"{(num+1):>2d}:{f.pretty_player_id(id):<12} " for num, id in enumerate(game.players)]

                # without seat num
                width = 12 if schedule.participants is not None else 2
                s = [
                    f"{f.pretty_player_id(id):<2} " for num, id in enumerate(game.players)]

                str = ''.join(s)
                if schedule.numTables > 1:
                    yield f"{f.pretty_table_id(table_id)}: {str}"
                else:
                    yield f"{str}"

    @ staticmethod
    def roundByGames(schedule: Schedule, round: Round):
        f = Format(schedule)

        yield f"\nRound: {f.pretty_round_id(round.id)}"
        for table_id, game_id in enumerate(round.gameIds):
            game = schedule.games[game_id]

            # without seat num
            width = 12 if schedule.participants is not None else 2
            s = [
                f"{f.pretty_player_id(id):<2} " for num, id in enumerate(game.players)]

            str = ''.join(s)
            if schedule.numTables > 1:
                yield f"{f.pretty_table_id(table_id)}: {str}"
            else:
                yield f"{str}"

    @ staticmethod
    def scheduleByGender(schedule: Schedule):
        if schedule.numTeams == 0:
            return
        f = Format(schedule)

        yield ''
        yield "Schedule by gender:"
        for round in schedule.rounds:
            yield f"\nRound: {f.pretty_round_id(round.id)}"
            for gameId in round.gameIds:
                game = schedule.games[gameId]
                # just for test!
                '''s = [
                    f"{Print.pretty_player_id(id)}" for id in game.players]
                str = ''.join(s)'''
                str = ''

                # for Boys/Girls only
                team_dict = defaultdict(int)
                for id in game.players:
                    idx = id // schedule.numTeams
                    team_dict[idx] += 1
                str += f"Boys: {team_dict[0]:2d} Girls: {team_dict[1]:2d}"

                yield f"Game {f.pretty_game_id(game.id)}: {str}"

    def playerTableHistogram(schedule: Schedule):
        f = Format(schedule)

        # init statistics: tables of every player
        player_tables = {}
        for player_id in range(schedule.numPlayers):
            zero_list = []
            for _ in range(schedule.numTables):
                zero_list.append(0)
            player_tables[player_id] = zero_list

        # calc table histogram for every player
        for round in schedule.rounds:
            for table_id, game_id in enumerate(round.gameIds):
                game = schedule.games[game_id]
                for player_id in game.players:
                    player_tables[player_id][table_id] += 1

        yield ''
        yield "Player table histogram:"

        for player_id in range(schedule.numPlayers):
            line = f"{f.pretty_player_id(player_id):<20}:  "
            tables = player_tables[player_id]
            for table_id, table_games in enumerate(tables):
                # line += f"{Print.pretty_table_id(table_id)}: {table_games:<2d} "
                line += f"{table_games:<2d}  "

            yield line

    @ staticmethod
    def scheduleByPlayers(schedule: Schedule):
        f = Format(schedule)
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

            header = f"{f.pretty_player_id(playerId):<20}: "
            yield f"{header}{str}"

    @ staticmethod
    def seatsMatrix(schedule: Schedule):
        f = Format(schedule)
        m = Metrics(schedule)
        matrix = m.calcSeatsMatrix()

        yield ''
        yield "*** Seats matrix:"
        for playerId in range(len(matrix)):
            line = matrix[playerId]
            s = ''.join([f"{v:3d}" for v in line])
            yield f"{f.pretty_player_id(playerId):<20}: {s}"

    @ staticmethod
    def mwtSchedule(schedule: Schedule):
        f = Format(schedule)
        for round in schedule.rounds:
            for seat in range(10):
                ids = [schedule.games[gameId].players[seat]
                       for gameId in round.gameIds]

                line = [f"{f.pretty_player_id(id):<12}," for id in ids]

                # print without last comma
                str = ''.join(line)
                yield str[:-1]
            yield ''
