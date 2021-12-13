import dataclasses
import unittest

from configuration import *


class TestConfiguration(unittest.TestCase):
    def test_configuration_CreateSimple(self):
        c = Configuration(33, 3, 11, 33, 10)
        self.assertEqual(c.numPlayers, 33)
        self.assertEqual(c.numTables, 3)
        self.assertEqual(c.numRounds, 11)
        self.assertEqual(c.numGames, 33)
        self.assertEqual(c.numAttempts, 10)

    def test_configuration_Readonly(self):
        c = Configuration(30, 3, 10, 30, 10)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            c.numPlayers = 40
        with self.assertRaises(dataclasses.FrozenInstanceError):
            c.numTables = 20
        with self.assertRaises(dataclasses.FrozenInstanceError):
            c.numRounds = 12
        with self.assertRaises(dataclasses.FrozenInstanceError):
            c.numGames = 8
        with self.assertRaises(dataclasses.FrozenInstanceError):
            c.numAttempts = 1

    def test_configuration_validate_oneTable(self):
        c = Configuration(numPlayers=12, numTables=1,
                          numRounds=6, numGames=6, numAttempts=5)
        self.assertTrue(c.isValid())

        c = Configuration(numPlayers=10, numTables=1,
                          numRounds=3, numGames=3, numAttempts=3)
        self.assertTrue(c.isValid())

    def test_configuration_validate_twoTables(self):
        c = Configuration(numPlayers=20, numTables=2,
                          numRounds=10, numGames=20, numAttempts=10)
        self.assertTrue(c.isValid())

        c = Configuration(numPlayers=25, numTables=2,
                          numRounds=10, numGames=20, numAttempts=8)
        self.assertTrue(c.isValid())

    def test_configuration_validate_threeTables(self):
        c = Configuration(numPlayers=30, numTables=3,
                          numRounds=10, numGames=30, numAttempts=10)
        self.assertTrue(c.isValid())

        c = Configuration(numPlayers=36, numTables=3,
                          numRounds=12, numGames=36, numAttempts=10)
        self.assertTrue(c.isValid())

        c = Configuration(numPlayers=37, numTables=3,
                          numRounds=13, numGames=37, numAttempts=10)
        self.assertTrue(c.isValid())

    def test_configuration_validate_fail_players(self):
        '''players must be >=10'''
        with self.assertRaises(ConfigurationException):
            c = Configuration(numPlayers=-1, numTables=1,
                              numRounds=10, numGames=10, numAttempts=10)
            c.validate()

        with self.assertRaises(ConfigurationException):
            c = Configuration(numPlayers=9, numTables=1,
                              numRounds=10, numGames=10, numAttempts=10)
            c.validate()

    def test_configuration_validate_fail_zeroValues(self):
        with self.assertRaises(ConfigurationException):
            c = Configuration(numPlayers=0, numTables=1,
                              numRounds=10, numGames=10, numAttempts=10)
            c.validate()

        with self.assertRaises(ConfigurationException):
            c = Configuration(numPlayers=10, numTables=0,
                              numRounds=10, numGames=10, numAttempts=10)
            c.validate()

        with self.assertRaises(ConfigurationException):
            c = Configuration(numPlayers=10, numTables=1,
                              numRounds=0, numGames=10, numAttempts=10)
            c.validate()

        with self.assertRaises(ConfigurationException):
            c = Configuration(numPlayers=10, numTables=1,
                              numRounds=10, numGames=0, numAttempts=10)
            c.validate()

        with self.assertRaises(ConfigurationException):
            c = Configuration(numPlayers=10, numTables=1,
                              numRounds=10, numGames=10, numAttempts=0)
            c.validate()

    def test_configuration_validate_gamesRoundsMatch(self):
        '''games must be in range [tables * rounds-1; rables * rounds]'''
        with self.assertRaises(ConfigurationException):
            # rounds must be 12 here
            c = Configuration(numPlayers=35, numTables=3,
                              numRounds=10, numGames=35, numAttempts=10)
            c.validate()

        with self.assertRaises(ConfigurationException):
            # rounds must be 12 here
            c = Configuration(numPlayers=35, numTables=3,
                              numRounds=13, numGames=35, numAttempts=10)
            c.validate()

    def test_configuration_validate_attemptsGamesMatch(self):
        '''players x attempts must be == games * 10'''
        with self.assertRaises(ConfigurationException):
            # attempts must be 10 here
            c = Configuration(numPlayers=35, numTables=3,
                              numRounds=12, numGames=35, numAttempts=8)
            c.validate()

        with self.assertRaises(ConfigurationException):
            # attempts must be 10 here
            c = Configuration(numPlayers=35, numTables=3,
                              numRounds=12, numGames=35, numAttempts=12)
            c.validate()


if __name__ == '__main__':
    unittest.main()
