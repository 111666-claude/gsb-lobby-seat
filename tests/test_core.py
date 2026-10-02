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


class SeatReuseTest(unittest.TestCase):
    def test_freed_seat_is_reused(self):
        room = Room(3)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("b")
        self.assertEqual(room.join("d"), 1)

    def test_smallest_free_seat_wins(self):
        room = Room(4)
        for player in ("a", "b", "c", "d"):
            room.join(player)
        room.leave("d")
        room.leave("b")
        self.assertEqual(room.join("e"), 1)
        self.assertEqual(room.join("f"), 3)

    def test_seat_stays_within_bounds(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        room.leave("a")
        self.assertEqual(room.join("c"), 0)
        self.assertIsNone(room.join("d"))


class QueueTest(unittest.TestCase):
    def test_extra_player_waits(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        self.assertIsNone(room.join("c"))
        self.assertEqual(room.waiting_list(), ["c"])

    def test_first_waiter_takes_freed_seat(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        room.join("c")
        room.join("d")
        room.leave("a")
        self.assertEqual(room.seat_of_player("c"), 0)
        self.assertEqual(room.waiting_list(), ["d"])

    def test_waiters_promoted_in_join_order(self):
        room = Room(1)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("a")
        self.assertEqual(room.seat_of_player("b"), 0)
        room.leave("b")
        self.assertEqual(room.seat_of_player("c"), 0)
        self.assertEqual(room.waiting_list(), [])

    def test_duplicate_join_while_waiting_stays_queued(self):
        room = Room(1)
        room.join("a")
        self.assertIsNone(room.join("b"))
        self.assertIsNone(room.join("b"))
        self.assertEqual(room.waiting_list(), ["b"])


class ReadyTest(unittest.TestCase):
    def test_ready_requires_a_seat(self):
        self.assertFalse(Room(2).ready("ghost"))

    def test_empty_room_cannot_start(self):
        self.assertFalse(Room(2).start())

    def test_start_requires_everyone_ready(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        room.ready("a")
        self.assertFalse(room.start())
        room.ready("b")
        self.assertTrue(room.start())

    def test_ready_resets_when_leaving(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        room.ready("a")
        room.ready("b")
        room.leave("b")
        self.assertFalse(room.start())

    def test_rejoin_after_leave_is_not_ready(self):
        room = Room(1)
        room.join("a")
        room.ready("a")
        room.leave("a")
        room.join("a")
        self.assertFalse(room.start())

    def test_promoted_player_is_not_ready(self):
        room = Room(1)
        room.join("a")
        room.ready("a")
        room.join("b")
        room.leave("a")
        self.assertNotIn("b", room.ready_set)
        self.assertFalse(room.start())


class HostTest(unittest.TestCase):
    def test_host_is_player_with_smallest_seat(self):
        room = Room(3)
        room.join("a")
        room.join("b")
        room.join("c")
        self.assertEqual(room.host(), "a")
        room.leave("a")
        self.assertEqual(room.host(), "b")
        room.leave("b")
        self.assertEqual(room.host(), "c")

    def test_host_follows_seat_not_join_order(self):
        room = Room(3)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("a")
        room.join("d")
        self.assertEqual(room.host(), "d")

    def test_empty_room_has_no_host(self):
        room = Room(2)
        self.assertIsNone(room.host())
        room.join("a")
        room.leave("a")
        self.assertIsNone(room.host())


class ScanTest(unittest.TestCase):
    def test_seat_query_cost_does_not_scale_with_players(self):
        room = Room(3000)
        for index in range(3000):
            room.join("p-%d" % index)
        before = room.scanned
        for _ in range(3000):
            room.seat_of_player("p-2999")
        self.assertLessEqual(room.scanned - before, 3000)


if __name__ == "__main__":
    unittest.main()
