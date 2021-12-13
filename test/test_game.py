import unittest

from game import Game
from player import Player, Participants


class TestGame(unittest.TestCase):
    def test_game_CreateEmpty(self):
        game = Game(7, [])
        self.assertEqual(game.id, 7)
        self.assertEqual(len(game.players), 0)
        self.assertFalse(game.isValid())

    def test_game_CreateSimple(self):
        participants = Participants.create(10)
        players = participants.people
        game = Game(1, players)
        self.assertEqual(len(game.players), 10)
        self.assertTrue(game.isValid())

    def test_game_isValid_WrongCount(self):
        participants = Participants.create(10)
        players = participants.people
        players = players[:-1]
        game = Game(1, players)

        self.assertEqual(len(game.players), 9)
        self.assertFalse(game.isValid())

    def test_game_isValid_NonUnique(self):
        # duplicate the fifth player
        participants = Participants.create(10)
        players = participants.people
        players[7] = players[5]

        game = Game(1, players)
        self.assertEqual(len(game.players), 10)
        self.assertFalse(game.isValid())

    pass


if __name__ == '__main__':
    unittest.main()
