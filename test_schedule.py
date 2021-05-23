import unittest
from schedule import Configuration
from schedule import Schedule

class TestSchedule(unittest.TestCase):
    def test_scheduleCreateEmpty(self):
        s = Schedule(None)
        self.assertEqual(s.configuration, None)
        self.assertEqual(s.players, [])
        self.assertEqual(s.rounds, [])
        self.assertEqual(s.games, [])

    def test_scheduleCreateConfiguration(self):
        config = Configuration(numPlayers=30, numTables=3, numRounds=10, numGames=30, numAttempts=10)
        s = Schedule(config)
        self.assertEqual(s.configuration, config)

        # this code is broken, need to initialize empty schedule first
        self.assertEqual(len(s.players), 30)
        self.assertEqual(len(s.rounds), 10)
        self.assertEqual(len(s.games), 30)
    
    pass

if __name__ == '__main__':
    unittest.main()