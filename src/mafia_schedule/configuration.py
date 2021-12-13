from dataclasses import dataclass


class ConfigurationException(Exception):
    pass


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

    def isValid(self) -> bool:
        try:
            self.validate()
        except ConfigurationException:
            return False
        return True

    def validate(self):
        if self.numPlayers < 10:
            raise ConfigurationException(
                f"numPlayers must by >= 10 (value: {self.numPlayers}")

        if self.numTables < 1:
            raise ConfigurationException(
                f"numTables must be >=1 (value: {self.numTables})")

        if self.numRounds < 1:
            raise ConfigurationException(
                f"numRounds must be >=1 (value: {self.numRounds})")

        if self.numGames < 1:
            raise ConfigurationException(
                f"numGames must be >=1 (value: {self.numGames})")

        if self.numAttempts < 1:
            raise ConfigurationException(
                f"numAttempts must be >=1 (value: {self.numAttempts})")

        numGamesLo = self.numTables * (self.numRounds - 1)
        numGamesHi = self.numTables * self.numRounds
        if self.numGames < numGamesLo or self.numGames > numGamesHi:
            raise ConfigurationException(
                f"numGames must be in range [{numGamesLo}, {numGamesHi}] (value: {self.numGames}]")

        if (self.numPlayers * self.numAttempts) % 10 != 0:
            raise ConfigurationException(
                f"numPlayers x numAttempts must be dividable by 10 (value: {self.numPlayers * self.numAttempts})")

        if (self.numPlayers * self.numAttempts) / 10 != self.numGames:
            raise ConfigurationException(
                f"numGames must match numPlayers x numAttempts (numGames: {self.numGames}, numPlayers: {self.numPlayers}, numAttempts: {self.numAttempts}")
