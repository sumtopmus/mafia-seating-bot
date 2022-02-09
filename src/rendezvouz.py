from mafia_schedule import *
from mafia_schedule.helpers import *


'''
Operations: manual set of flips and swaps to create beautiful schedule
for team Men/Woman tournament.
Flip: swap team members (m <-> f)
Swap: swap members of different teams (but same gender!)
'''
operations = {
    0: [],

    # flip 0
    1: [
        {'type': 'flip', 'table_one': 0, 'table_two': 2, 'seat': 0},
        {'type': 'flip', 'table_one': 1, 'table_two': 3, 'seat': 0},

        # swap before jumping to other gender table
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 1},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 1},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 8},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 8},

    ],

    # flip 1
    2: [
        {'type': 'flip', 'table_one': 0, 'table_two': 2, 'seat': 1},
        {'type': 'flip', 'table_one': 1, 'table_two': 3, 'seat': 1},

        # swap before jumping to other gender table
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 2},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 2},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 3},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 3},

    ],

    # flip 2
    3: [
        {'type': 'flip', 'table_one': 0, 'table_two': 2, 'seat': 2},
        {'type': 'flip', 'table_one': 1, 'table_two': 3, 'seat': 2},

        # make for player 4: 3-3 before jumping
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 4},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 4},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 7},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 7},

    ],

    # swap only boys/girls
    4: [
        # swap minorities
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 0},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 0},
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 1},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 1},
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 2},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 2},
    ],

    # flip 3
    5: [
        {'type': 'flip', 'table_one': 0, 'table_two': 2, 'seat': 3},
        {'type': 'flip', 'table_one': 1, 'table_two': 3, 'seat': 3},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 6},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 6},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 9},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 9},

    ],

    # flip 4
    6: [
        {'type': 'flip', 'table_one': 0, 'table_two': 2, 'seat': 4},
        {'type': 'flip', 'table_one': 1, 'table_two': 3, 'seat': 4},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 5},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 5},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 8},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 8},

    ],

    # swap in even case1
    7: [
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 1},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 1},

        # make for player7: play 5-6 before jump
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 7},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 7},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 9},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 9},

    ],

    # swap in even case2
    8: [{'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 0},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 0},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 3},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 3},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 8},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 8},

        ],

    # flip 5
    9: [
        {'type': 'flip', 'table_one': 0, 'table_two': 2, 'seat': 5},
        {'type': 'flip', 'table_one': 1, 'table_two': 3, 'seat': 5},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 2},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 2},

        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 4},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 4},
    ],

    # flip 6
    10: [{'type': 'flip', 'table_one': 0, 'table_two': 2, 'seat': 6},
         {'type': 'flip', 'table_one': 1, 'table_two': 3, 'seat': 6},

         # swap after  jumping
         {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 5},
         {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 5},

         # make for player3: 5-5 after jumping
         {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 3},
         {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 3}
         ],

    # swap before final flip
    11: [
        # swap minorities
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 7},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 7},
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 8},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 8},
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 9},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 9},
    ],

    # flip 7
    12: [
        {'type': 'flip', 'table_one': 0, 'table_two': 2, 'seat': 7},
        {'type': 'flip', 'table_one': 1, 'table_two': 3, 'seat': 7},

        # swap
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 0},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 0},

        # swap after jumping
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 6},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 6},
    ],

    # flip 8
    13: [
        {'type': 'flip', 'table_one': 0, 'table_two': 2, 'seat': 8},
        {'type': 'flip', 'table_one': 1, 'table_two': 3, 'seat': 8},


        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 1},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 1},

        # swap right after jumping
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 7},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 7},
    ],

    # flip 9
    14: [
        {'type': 'flip', 'table_one': 0, 'table_two': 2, 'seat': 9},
        {'type': 'flip', 'table_one': 1, 'table_two': 3, 'seat': 9},

        # swap right after jumping
        {'type': 'swap', 'table_one': 0, 'table_two': 1, 'seat': 8},
        {'type': 'swap', 'table_one': 2, 'table_two': 3, 'seat': 8},
    ],
}


def flipTeamPlayers(conf: Configuration, gameOne: Game, gameTwo: Game, seat: int):
    playerOne = gameOne.players[seat]
    playerTwo = gameTwo.players[seat]

    team_one = playerOne % conf.numTeams
    team_two = playerTwo % conf.numTeams
    if team_one != team_two:
        raise RuntimeError(
            "Flipping players from different teams in seat {seat}. Game1: {gameOne.id}/{playerOne}. Game2: {gameTwo.id}/{playerTwo}")

    gameOne.players[seat] = playerTwo
    gameTwo.players[seat] = playerOne


def swapPlayers(conf: Configuration, gameOne: Game, gameTwo: Game, seat: int):
    playerOne = gameOne.players[seat]
    playerTwo = gameTwo.players[seat]

    team_shift_one = playerOne // conf.numTeams
    team_shift_two = playerTwo // conf.numTeams
    if team_shift_one != team_shift_two:
        raise RuntimeError(
            "Swapping players from different genders in seat {seat}. Game1: {gameOne.id}/{playerOne}. Game2: {gameTwo.id}/{playerTwo}")

    gameOne.players[seat] = playerTwo
    gameTwo.players[seat] = playerOne


def execute_operation(operation: dict, conf: Configuration, round: Round, all_games: list[Game]):
    if operation['type'] == 'flip':
        game_one = round.gameIds[operation['table_one']]
        game_two = round.gameIds[operation['table_two']]
        seat = operation['seat']
        flipTeamPlayers(conf, all_games[game_one], all_games[game_two], seat)
    elif operation['type'] == 'swap':
        game_one = round.gameIds[operation['table_one']]
        game_two = round.gameIds[operation['table_two']]
        seat = operation['seat']
        swapPlayers(conf, all_games[game_one], all_games[game_two], seat)
        pass
    else:
        raise RuntimeError("Unknown operation type: {operation['type']")


def createFirstRound(conf: Configuration):
    games = []
    game_ids = []
    for game_id in range(conf.numTables):
        player_ids = list(range(game_id * 10, (game_id+1) * 10))
        game = Game(game_id, player_ids)
        games.append(game)
        game_ids.append(game.id)

    round_id = 0
    round = Round(round_id, game_ids)

    return round, games


def copyRound(conf: Configuration, all_rounds: Round, all_games: list[Game]):
    prev_game_id = (len(all_rounds)-1) * conf.numTables
    start_game_id = len(all_rounds) * conf.numTables

    games = []
    game_ids = []
    for game_id in range(conf.numTables):
        player_ids = all_games[prev_game_id + game_id].players
        game = Game(start_game_id + game_id, player_ids.copy())
        games.append(game)
        game_ids.append(game.id)

    round_id = len(all_rounds)
    round = Round(round_id, game_ids)

    return round, games


def createRendezVouzSchedule(conf: Configuration):
    if not conf.isValid():
        return None

    all_rounds = []
    all_games = []

    first_round, first_games = createFirstRound(conf)
    all_rounds.append(first_round)
    all_games.extend(first_games)

    for round_id in range(1, conf.numRounds):
        # copy round from previous one
        round, games = copyRound(conf, all_rounds, all_games)
        all_rounds.append(round)
        all_games.extend(games)

        # apply manual operations
        for op in operations[round_id]:
            execute_operation(op, conf, round, all_games)

    schedule = Schedule(conf, all_rounds, all_games)
    return schedule
