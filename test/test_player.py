import dataclasses
import unittest

from player import *


class TestPlayer(unittest.TestCase):
    def setUp(self):
        # print("Before test")
        pass

    def tearDown(self):
        # print("After test")
        pass

    def test_player_Create(self):
        player = Player(1, 'Nickname')
        self.assertEqual(player.id, 1)
        self.assertEqual(player.name, 'Nickname')

    def test_player_CreateIntName(self):
        '''
        Unfortunately, it is still possible to create player with integer (non string!) name
        '''
        player = Player(147, 42)
        self.assertEqual(player.id, 147)
        self.assertEqual(player.name, 42)

    def test_player_IdReadonly(self):
        player = Player(1, 'name')
        self.assertEqual(player.id, 1)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            player.id = 2

    def test_player_NameReadonly(self):
        player = Player(1, 'docent')
        self.assertEqual(player.name, 'docent')
        with self.assertRaises(dataclasses.FrozenInstanceError):
            player.name = 'like'

    pass


if __name__ == '__main__':
    unittest.main()
