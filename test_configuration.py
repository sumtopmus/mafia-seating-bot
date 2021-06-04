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


if __name__ == '__main__':
    unittest.main()
