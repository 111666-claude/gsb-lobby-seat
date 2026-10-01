import unittest

from lobby.core import Room


class SeatTest(unittest.TestCase):
    def test_seats_are_numbered_from_zero(self):
        room = Room(3)
        self.assertEqual(room.join("a"), 0)
        self.assertEqual(room.join("b"), 1)

    def test_duplicate_join_returns_same_seat(self):
        room = Room(3)
        room.join("a")
        self.assertEqual(room.join("a"), 0)

    def test_unknown_player_has_no_seat(self):
        self.assertIsNone(Room(3).seat_of_player("ghost"))


class QueueTest(unittest.TestCase):
    def test_extra_player_waits(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        self.assertIsNone(room.join("c"))
        self.assertEqual(room.waiting_list(), ["c"])


class ReadyTest(unittest.TestCase):
    def test_ready_requires_a_seat(self):
        self.assertFalse(Room(2).ready("ghost"))

    def test_empty_room_cannot_start(self):
        self.assertFalse(Room(2).start())


if __name__ == "__main__":
    unittest.main()
