import unittest
from player import *

class TestParticipants(unittest.TestCase):

    def test_participants_generateNames(self):
        names = Participants.generateNames(3)
        self.assertEqual(names, ["Player_1", "Player_2", "Player_3"])

    def test_participants_generageNamesWithCustomPrefix(self):
        names = Participants.generateNames(2, "prefix")
        self.assertEqual(names, ["prefix1", "prefix2"])

    def test_participantsCreate(self):
        names = ['like', 'aman', 'fantomas']
        people = Participants(names)
        self.assertEqual(len(people), 3)

        self.assertEqual(people[0].id, 0)
        self.assertEqual(people[0].name, 'like')

        self.assertEqual(people[1].id, 1)
        self.assertEqual(people[1].name, 'aman')

        self.assertEqual(people[2].id, 2)
        self.assertEqual(people[2].name, 'fantomas')

    pass


if __name__ == '__main__':
    unittest.main()
