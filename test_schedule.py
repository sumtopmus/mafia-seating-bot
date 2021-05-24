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
        conf = Configuration(numPlayers = 10, numTables = 1, numRounds = 1, numGames = 1, numAttempts = 1)
        participants = Participants.create(10)
        game = Game(1, participants.all)
        rounds = [Round(1, [game])]

        s = Schedule(conf, participants, rounds)
        self.assertEqual(s.configuration, conf)
        self.assertEqual(len(s.participants), 10)
        self.assertEqual(len(s.rounds), 1)
        self.assertEqual(len(s.games), 1)
    
    pass

if __name__ == '__main__':
    unittest.main()