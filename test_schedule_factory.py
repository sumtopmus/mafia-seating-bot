import unittest

from schedule_factory import *
from schedule import *
from round import *
from game import *
from player import *


class TestScheduleFactory(unittest.TestCase):
    def test_factory_simple(self):
        '''
        Simple schedule: 10 players, just 1 game
        '''
        conf = Configuration(numPlayers=10, numTables=1,
                             numRounds=1, numGames=1, numAttempts=1)
        s = ScheduleFactory.createInitialSchedule(conf)
        self.assertTrue(s.isValid())

    def test_factory_simple_bad(self):
        '''
        Bad schedule: 11 players, just 1 game
        '''
        conf = Configuration(numPlayers=11, numTables=1,
                             numRounds=1, numGames=1, numAttempts=1)
        self.assertFalse(conf.isValid())
        s = ScheduleFactory.createInitialSchedule(conf)
        self.assertTrue(s == None)

    def test_factory_rounds2_players10_attempts2(self):
        '''
        Simple 2-round schedule: 10 players 2 attempts per player
        '''
        conf = Configuration(numPlayers=10, numTables=1,
                             numRounds=2, numGames=2, numAttempts=2)
        s = ScheduleFactory.createInitialSchedule(conf)
        self.assertTrue(s.isValid())

    def test_factory_rounds2_players20_attempts1(self):
        '''
        Simple 2-round schedule: 20 players 1 attempts per player
        '''
        conf = Configuration(numPlayers=20, numTables=1,
                             numRounds=2, numGames=2, numAttempts=1)
        s = ScheduleFactory.createInitialSchedule(conf)
        self.assertTrue(s.isValid())

    def test_factory_tables1_players12(self):
        '''
        Classic mini-tournament schedule
        '''
        conf = Configuration(numPlayers=12, numTables=1,
                             numRounds=6, numGames=6, numAttempts=5)
        s = ScheduleFactory.createInitialSchedule(conf)
        self.assertTrue(s.isValid())

    def test_factory_tables2_players20(self):
        '''
        Full schedule for 2 tables
        '''
        conf = Configuration(numPlayers=20, numTables=2,
                             numRounds=10, numGames=20, numAttempts=10)
        s = ScheduleFactory.createInitialSchedule(conf)
        self.assertTrue(s.isValid())

    def test_factory_tables2_players25(self):
        '''
        Not-full schedule for 2 tables (VaWaCa-2017)
        '''
        conf = Configuration(numPlayers=25, numTables=2,
                             numRounds=10, numGames=20, numAttempts=8)
        s = ScheduleFactory.createInitialSchedule(conf)
        self.assertTrue(s.isValid())

    def test_factory_tables3_players30(self):
        '''
        Full schedule for 3 tables
        '''
        conf = Configuration(numPlayers=30, numTables=3,
                             numRounds=10, numGames=30, numAttempts=10)
        s = ScheduleFactory.createInitialSchedule(conf)
        self.assertTrue(s.isValid())

    def test_factory_tables3_players33(self):
        '''
        Not-full schedule for 3 tables (11 rounds by 10 attempts per player)
        '''
        conf = Configuration(numPlayers=33, numTables=3,
                             numRounds=11, numGames=33, numAttempts=10)
        s = ScheduleFactory.createInitialSchedule(conf)
        self.assertTrue(s.isValid())

    def test_factory_tables3_players35(self):
        '''
        Not-full schedule for 3 tables with not all tables at the last round (12 rounds by 10 attempts per player)
        '''
        conf = Configuration(numPlayers=35, numTables=3,
                             numRounds=12, numGames=35, numAttempts=10)
        s = ScheduleFactory.createInitialSchedule(conf)
        self.assertTrue(s.isValid())


if __name__ == '__main__':
    unittest.main()
