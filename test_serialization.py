import dataclasses
import unittest
import json

from configuration import *
from schedule import *
from schedule_factory import *
from player import *
from game import *

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
        participants = Participants.create(3)
        d = dataclasses.asdict(participants)
        self.assertEqual(d, {'people': [
            {'id': 0, 'name': 'Player_0'},
            {'id': 1, 'name': 'Player_1'},
            {'id': 2, 'name': 'Player_2'}]
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
        participants = Participants.create(10)
        players = participants.people
        game = Game(525, players)
        d = dataclasses.asdict(game)
        expected = {'id': 525, 'players': [dataclasses.asdict(player) for player in players]}
        self.assertEqual(d, expected)

    def test_game_fromJson(self):
        playerLike = Player(112, 'like')
        playerAman = Player(113, 'aman')
        d = {'id': 525,
             'players': [
                 {'id': playerLike.id, 'name': playerLike.name},
                 {'id': playerAman.id, 'name': playerAman.name}
             ]}

        game = Game.fromJson(d)
        self.assertEqual(game.id, 525)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.players[0], playerLike)
        self.assertEqual(game.players[1], playerAman)

    def test_round_toJson(self):
        participants = Participants.create(10)
        players = participants.people
        game1 = Game(525, players)
        games = [game1]
        round = Round(727, games)
        d = dataclasses.asdict(round)
        self.assertEqual(
            d, {'id': 727, 'games': [dataclasses.asdict(game) for game in games]})

    def test_round_fromJson(self):
        participants = Participants.create(10)
        players = participants.people
        game1 = Game(525, players)
        game2 = Game(727, players)
        games = [game1, game2]

        d = {'id': 100, 'games': [dataclasses.asdict(game) for game in games]}
        round = Round.fromJson(d)

        self.assertEqual(round.id, 100)
        self.assertEqual(len(round.games), 2)
        self.assertEqual(round.games[0].id, 525)
        self.assertEqual(round.games[1].id, 727)

    def test_schedule_toJson(self):
        numPlayers = 10
        participants = Participants.create(numPlayers)

        conf = Configuration(numPlayers, numTables=1,
                             numRounds=1, numGames=1, numAttempts=1)
        schedule = ScheduleFactory.createInitialSchedule(conf, participants)
        d = schedule.toJson()
        self.assertEqual(d, {'configuration': dataclasses.asdict(conf),
                             'participants': dataclasses.asdict(participants),
                             'rounds': [dataclasses.asdict(round) for round in schedule.rounds]})

    pass


if __name__ == '__main__':
    unittest.main()