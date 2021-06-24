import unittest
from schedule import Configuration
from schedule import *
from player import *
from game import *

class TestSchedule(unittest.TestCase):
    def test_schedule_CreateEmpty(self):
        s = Schedule(None)
        self.assertEqual(s.configuration, None)
        self.assertEqual(s.participants, None)
        self.assertEqual(s.rounds, [])
        self.assertEqual(s.games, [])

    def test_schedule_CreateSimple(self):
        numPlayers = 10
        conf = Configuration(numPlayers, numTables = 1, numRounds = 1, numGames = 1, numAttempts = 1)
        game = Game(1, list(range(numPlayers)))
        games = [game]
        rounds = [Round(1, [game.id])]

        s = Schedule(conf, rounds, games)
        self.assertEqual(s.configuration, conf)
        self.assertEqual(s.participants, None)
        self.assertEqual(len(s.rounds), 1)
        self.assertEqual(len(s.games), 1)
    
    pass

if __name__ == '__main__':
    unittest.main()