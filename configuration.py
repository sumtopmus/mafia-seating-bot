from dataclasses import dataclass


@dataclass(frozen=True)
class Configuration:
    '''
    Configuration - set of parameters for Mafia tournament
    '''
    # Number of players in tournament
    numPlayers: int

    # Number of tables (games in parallel)
    numTables: int

    # Number of rounds in tournament
    numRounds: int

    # Total number of games: up to  (NumTables * NumRounds)
    numGames: int

    # Total number of games for every player
    numAttempts: int
