class Configuration:
    '''
    Configuration - set of parameters for Mafia tournament
    '''
    # Number of players in tournament
    NumPlayers: int

    # Number of tables (games in parallel)
    NumTables: int

    # Number of rounds in tournament
    NumRounds: int

    # Total number of games: up to  (NumTables * NumRounds)
    NumGames: int

    # Total number of games for every player
    NumAttempts: int

    # full constructor
    def __init__(self, numPlayers, numTables, numRounds, numGames, numAttempts):
        self.NumPlayers = numPlayers
        self.NumTables = numTables
        self.NumRounds = numRounds
        self.NumGames = numGames
        self.NumAttempts = numAttempts

    def toJson(self) -> dict:
        return {"numPlayers": self.NumPlayers,
                "numTables": self.NumTables,
                "numRounds": self.NumRounds,
                "numGames": self.NumGames,
                "numAttempts": self.NumAttempts}

    @staticmethod
    def fromJson(d: dict):
        return Configuration(numPlayers=d["numPlayers"],
                             numTables=d["numTables"],
                             numRounds=d["numRounds"],
                             numGames=d["numGames"],
                             numAttempts=d["numAttempts"])

    pass
