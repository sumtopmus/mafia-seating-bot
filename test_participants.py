import unittest
from player import *

class TestParticipants(unittest.TestCase):

    def test_participants_generateNames(self):
        names = Participants.generateNames(3)
        self.assertEqual(names, ["Player_0", "Player_1", "Player_2"])

    def test_participants_generageNamesWithCustomPrefix(self):
        names = Participants.generateNames(2, "prefix")
        self.assertEqual(names, ["prefix0", "prefix1"])

    def test_participantsCreateFromNames(self):
        names = ["like", "aman", "fantomas"]
        people = Participants.createFromNames(names)
        self.assertEqual(len(people), 3)

        self.assertEqual(people[0].id, 0)
        self.assertEqual(people[0].name, "like")

        self.assertEqual(people[1].id, 1)
        self.assertEqual(people[1].name, "aman")

        self.assertEqual(people[2].id, 2)
        self.assertEqual(people[2].name, "fantomas")

    def test_participantsCreateFromPlayers(self):
        player0 = Player(525, "like")
        player1 = Player(727, "aman")
        player2 = Player(123, "fantomas")
        players = [player0, player1, player2]

        people = Participants(players)
        self.assertEqual(len(people), 3)

        self.assertEqual(people[0].id, player0.id)
        self.assertEqual(people[0].name, player0.name)

        self.assertEqual(people[1].id, player1.id)
        self.assertEqual(people[1].name, player1.name)

        self.assertEqual(people[2].id, player2.id)
        self.assertEqual(people[2].name, player2.name)

    pass


if __name__ == '__main__':
    unittest.main()
