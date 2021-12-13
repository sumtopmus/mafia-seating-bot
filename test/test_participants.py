import unittest

from player import Player, Participants


class TestParticipants(unittest.TestCase):

    def test_participants_generateNames(self):
        names = Participants.generateNames(3)
        self.assertEqual(names, ['p00', 'p01', 'p02'])

    def test_participants_generageNamesWithCustomPrefix(self):
        names = Participants.generateNames(2, 'prefix')
        self.assertEqual(names, ['prefix00', 'prefix01'])

    def test_participantsCreateFromNames(self):
        names = ['like', 'aman', 'fantomas']
        people = Participants.createFromNames(names)
        self.assertEqual(len(people), 3)

        self.assertEqual(people[0].id, 0)
        self.assertEqual(people[0].name, 'like')
        self.assertEqual(people[1].id, 1)
        self.assertEqual(people[1].name, 'aman')
        self.assertEqual(people[2].id, 2)
        self.assertEqual(people[2].name, 'fantomas')

    def test_participantsCreateFromPlayers(self):
        player0 = Player(525, 'like')
        player1 = Player(727, 'aman')
        player2 = Player(123, 'fantomas')
        players = [player0, player1, player2]

        people = Participants(players)
        self.assertEqual(len(people), 3)

        self.assertEqual(people[0], player0)
        self.assertEqual(people[1], player1)
        self.assertEqual(people[2], player2)

    def test_participants_find_ok(self):
        player0 = Player(525, 'like')
        player1 = Player(727, 'aman')
        player2 = Player(123, 'fantomas')
        players = [player0, player1, player2]
        people = Participants(players)

        self.assertEqual(people.find(525), player0)
        self.assertEqual(people.find(123), player2)
        self.assertEqual(people.find(727), player1)

    def test_participants_find_fail(self):
        player0 = Player(525, 'like')
        player1 = Player(727, 'aman')
        player2 = Player(123, 'fantomas')
        players = [player0, player1, player2]
        people = Participants(players)

        p = people.find(100)
        self.assertEqual(p, None)

    pass


if __name__ == '__main__':
    unittest.main()
