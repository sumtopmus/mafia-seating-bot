import unittest
from game import Game
from players import Players


class TestGame(unittest.TestCase):
    def setUp(self):
        names = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10"]
        self.allPlayers = Players(names).players

    def tearDown(self):
        del self.allPlayers

    def test_game_CreateEmpty(self):
        game = Game([])
        self.assertEqual(len(game.players), 0)
        self.assertFalse(game.isValid())

    def test_game_CreateSimple(self):
        game = Game(self.allPlayers)
        self.assertEqual(len(game.players), 10)
        self.assertTrue(game.isValid())

    def test_game_isValid_WrongCount(self):
        players = self.allPlayers[:-1]
        game = Game(players)

        self.assertEqual(len(game.players), 9)
        self.assertFalse(game.isValid())

    def test_game_isValid_NonUnique(self):
        # duplicate the fifth player
        players = self.allPlayers
        players[7] = players[5]

        game = Game(players)
        self.assertEqual(len(game.players), 10)
        self.assertFalse(game.isValid())

    pass

if __name__ == '__main__':
    unittest.main()
