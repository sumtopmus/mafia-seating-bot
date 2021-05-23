import unittest
from players import Players

class TestPlayers(unittest.TestCase):
    def test_playersCreate(self):
        names = ['like', 'aman', 'fantomas']
        players = Players(names)
        self.assertEqual(len(players.players), 3)

        self.assertEqual(players.players[0].id, 1)
        self.assertEqual(players.players[0].name, 'like')

        self.assertEqual(players.players[1].id, 2)
        self.assertEqual(players.players[1].name, 'aman')

        self.assertEqual(players.players[2].id, 3)
        self.assertEqual(players.players[2].name, 'fantomas')

    pass


if __name__ == '__main__':
    unittest.main()
