from collections import defaultdict
from typing import Callable

from .schedule import Schedule
from .metrics import Metrics


class Print:
    @staticmethod
    def print(func: Callable):
        for line in func:
            print(line)

    @staticmethod
    def pretty_player_id(player_id: int) -> str:
        # just for TEAMS - revert it back!!!
        # return f"{(player_id+1): >03d}"

        # just temp for RendezVouz
        numTeams = 20
        team_id = player_id % numTeams
        player_in_team = player_id // numTeams
        player_str = chr(ord('x') + player_in_team)
        return f"{(team_id+1):>2d}-{player_str}"

    @ staticmethod
    def pretty_team_id(player_id: int, numTeams: int) -> str:
        team_id = (player_id // numTeams) + 1
        team_shift = (player_id % numTeams) + 1
        return f"{team_id+1}{team_shift}"

    @ staticmethod
    def pretty_round_id(round_id: int) -> str:
        return f"{(round_id+1):>02d}"

    @ staticmethod
    def pretty_game_id(game_id: int) -> str:
        return f"{(game_id+1):>02d}"

    @staticmethod
    def pretty_table_id(table_id: int) -> str:
        return chr(ord('A') + table_id)

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
        m = Metrics(schedule)
        matrix = m.calcOpponentsMatrix()

        yield ''
        yield "*** Opponents matrix:"
        for playerId in range(len(matrix)):
            line = matrix[playerId]
            s = ''.join([f"{v:3d}" for v in line])
            yield f"{Print.pretty_player_id(playerId)}: {s}"

    @ staticmethod
    def pairsMatrix(schedule: Schedule):
        m = Metrics(schedule)

        yield ''
        yield "Pairs matrix:"
        for playerId in range(schedule.numPlayers):
            pairs = m.calcPlayerPairsHistogram(playerId)
            penalty = m.penaltyPlayer(playerId)
            header = f"Player {Print.pretty_player_id(playerId)}: err={penalty:6.2f}: "
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

            header = f"Player {Print.pretty_player_id(playerId)}: "
            str = ""
            for idx in numGames:
                if idx >= len(pairs) or len(pairs[idx]) == 0:
                    continue
                s = ''.join([f"{id:2d} " for id in pairs[idx]]
                            ) if len(pairs[idx]) < 5 else "..."
                str += f"g = {idx} with: [{s}]; "
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
        yield ''
        yield "Schedule by games:"
        for round in schedule.rounds:
            yield f"\nRound: {Print.pretty_round_id(round.id)}"
            for gameId in round.gameIds:
                game = schedule.games[gameId]
                s = [
                    f"{Print.pretty_player_id(id)} " for id in game.players]
                str = ''.join(s)
                yield f"Game {Print.pretty_game_id(game.id)}: {str}"

    @ staticmethod
    def scheduleByGender(schedule: Schedule):
        yield ''
        yield "Schedule by gender:"
        for round in schedule.rounds:
            yield f"\nRound: {Print.pretty_round_id(round.id)}"
            for gameId in round.gameIds:
                game = schedule.games[gameId]
                # just for test!
                '''s = [
                    f"{Print.pretty_player_id(id)}" for id in game.players]
                str = ''.join(s)'''
                str = ''

                # for Boys/Girls only
                numTeams = 20
                team_dict = defaultdict(int)
                for id in game.players:
                    idx = id // numTeams
                    team_dict[idx] += 1
                str += f"Boys: {team_dict[0]:2d} Girls: {team_dict[1]:2d}"

                yield f"Game {Print.pretty_game_id(game.id)}: {str}"

    def playerTableHistogram(schedule: Schedule):
        # init statistics: tables of every player
        player_tables = {}
        for player_id in range(schedule.numPlayers):
            zero_list = []
            for _ in range(schedule.numTables):
                zero_list.append(0)
            player_tables[player_id] = zero_list

        # calc table histogram for every player
        for round in schedule.rounds:
            for game_id in round.gameIds:
                game = schedule.games[game_id]
                table_id = game_id % schedule.configuration.numTables
                for player_id in game.players:
                    player_tables[player_id][table_id] += 1

        yield ''
        yield "Player table histogram:"

        for player_id in range(schedule.numPlayers):
            line = f"Player {Print.pretty_player_id(player_id)}:  "
            tables = player_tables[player_id]
            for table_id, table_games in enumerate(tables):
                # line += f"{Print.pretty_table_id(table_id)}: {table_games:<2d} "
                line += f"{table_games:<2d}  "

            yield line

    @ staticmethod
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
                header = f"Player {Print.pretty_player_id(playerId)}: "
            else:
                playerName = schedule.participants[playerId].name
                header = f"{playerName:20}:"
            yield f"{header}{str}"

    @ staticmethod
    def seatsMatrix(schedule: Schedule):
        m = Metrics(schedule)
        matrix = m.calcSeatsMatrix()

        yield ''
        yield "*** Seats matrix:"
        for playerId in range(len(matrix)):
            line = matrix[playerId]
            s = ''.join([f"{v:3d}" for v in line])
            yield f"{Print.pretty_player_id(playerId)}: {s}"

    @ staticmethod
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
