import dataclasses
import unittest
import json

from mafia_schedule.configuration import Configuration
from mafia_schedule.schedule_factory import ScheduleFactory
from mafia_schedule.schedule import Schedule
from mafia_schedule.round import Round
from mafia_schedule.game import Game
from mafia_schedule.player import Player, Participants


class TestSerialization(unittest.TestCase):
    def test_configuration_toJson(self):
        conf = Configuration(numPlayers=25, numTables=2,
                             numRounds=10, numGames=20, numAttempts=8)
        d = dataclasses.asdict(conf)
        self.assertEqual(d, {'numPlayers': 25,
                             'numTables': 2,
                             'numRounds': 10,
                             'numGames': 20,
                             'numAttempts': 8})

    def test_configuration_fromJson(self):
        d = {'numPlayers': 25,
             'numTables': 2,
             'numRounds': 10,
             'numGames': 20,
             'numAttempts': 8}
        conf = Configuration(**d)
        self.assertEqual(conf.numPlayers, 25)
        self.assertEqual(conf.numTables, 2)
        self.assertEqual(conf.numRounds, 10)
        self.assertEqual(conf.numGames, 20)
        self.assertEqual(conf.numAttempts, 8)

    def test_player_toJson(self):
        player = Player(525, 'like')
        d = dataclasses.asdict(player)
        self.assertEqual(d, {'id': 525, 'name': 'like'})

    def test_player_fromJson(self):
        d = {'id': 525, 'name': 'like'}
        player = Player(**d)
        self.assertEqual(player.id, 525)
        self.assertEqual(player.name, 'like')

    def test_participants_toJson(self):
        participants = Participants.create(3, "Player_")
        d = participants.toJson()
        self.assertEqual(d, {'people': [
            {'id': 0, 'name': 'Player_00'},
            {'id': 1, 'name': 'Player_01'},
            {'id': 2, 'name': 'Player_02'}]
        })

    def test_participants_fromJson(self):
        d = {'people': [
            {'id': 0, 'name': 'Player_0'},
            {'id': 1, 'name': 'Player_1'},
            {'id': 2, 'name': 'Player_2'}]
        }

        p = Participants.fromJson(d)
        self.assertEqual(p[0].id, 0)
        self.assertEqual(p[0].name, 'Player_0')
        self.assertEqual(p[1].id, 1)
        self.assertEqual(p[1].name, 'Player_1')
        self.assertEqual(p[2].id, 2)
        self.assertEqual(p[2].name, 'Player_2')

    def test_game_toJson(self):
        ids = [5, 9, 3, 6, 1, 4, 7, 8, 2, 0]
        game = Game(525, ids)
        d = dataclasses.asdict(game)
        expected = {'id': 525, 'players': ids}
        self.assertEqual(d, expected)

    def test_game_fromJson(self):
        playerLike = Player(112, 'like')
        playerAman = Player(113, 'aman')
        d = {'id': 525,
             'players': [112, 113]}

        game = Game.fromJson(d)
        self.assertEqual(game.id, 525)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.players[0], playerLike.id)
        self.assertEqual(game.players[1], playerAman.id)

    def test_round_toJson(self):
        participants = Participants.create(10)
        players = participants.people
        game1 = Game(525, players)
        games = [525]
        round = Round(727, games)
        d = dataclasses.asdict(round)
        self.assertEqual(
            d, {'id': 727, 'gameIds': [525]})

    def test_round_fromJson(self):
        participants = Participants.create(10)
        players = participants.people
        game1 = Game(525, players)
        game2 = Game(727, players)
        gameIds = [game1.id, game2.id]

        d = {'id': 100, 'gameIds': [525, 727]}
        round = Round.fromJson(d)

        self.assertEqual(round.id, 100)
        self.assertEqual(len(round.gameIds), 2)
        self.assertEqual(round.gameIds[0], 525)
        self.assertEqual(round.gameIds[1], 727)

    def test_schedule_toJson(self):
        numPlayers = 10
        conf = Configuration(numPlayers, numTables=1,
                             numRounds=1, numGames=1, numAttempts=1)
        schedule = ScheduleFactory.createInitialSchedule(conf)
        d = schedule.toJson()
        self.assertEqual(d, {'configuration': dataclasses.asdict(conf),
                             'rounds': [dataclasses.asdict(round) for round in schedule.rounds],
                             'games': [dataclasses.asdict(game) for game in schedule.games]})

    pass


if __name__ == '__main__':
    unittest.main()
