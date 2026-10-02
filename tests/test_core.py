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

    def test_freed_seat_is_reused_with_lowest_number(self):
        room = Room(3)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("b")
        self.assertEqual(room.join("d"), 1)
        self.assertEqual(room.seat_of_player("d"), 1)

    def test_seat_numbers_stay_in_range(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        room.leave("a")
        room.leave("b")
        self.assertEqual(room.join("c"), 0)
        self.assertEqual(room.join("d"), 1)


class QueueTest(unittest.TestCase):
    def test_extra_player_waits(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        self.assertIsNone(room.join("c"))
        self.assertEqual(room.waiting_list(), ["c"])

    def test_leaver_promotes_first_waiter_into_freed_seat(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("a")
        self.assertEqual(room.seat_of_player("c"), 0)
        self.assertEqual(room.waiting_list(), [])

    def test_promotion_is_first_come_first_served(self):
        room = Room(1)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("a")
        self.assertEqual(room.seat_of_player("b"), 0)
        self.assertEqual(room.waiting_list(), ["c"])

    def test_waiting_player_can_leave(self):
        room = Room(1)
        room.join("a")
        room.join("b")
        self.assertTrue(room.leave("b"))
        self.assertEqual(room.waiting_list(), [])


class ReadyTest(unittest.TestCase):
    def test_ready_requires_a_seat(self):
        self.assertFalse(Room(2).ready("ghost"))

    def test_empty_room_cannot_start(self):
        self.assertFalse(Room(2).start())

    def test_start_needs_all_seated_and_ready(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        room.ready("a")
        self.assertFalse(room.start())
        room.ready("b")
        self.assertTrue(room.start())

    def test_leave_resets_ready_state(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        room.ready("a")
        room.ready("b")
        room.leave("b")
        room.join("c")
        self.assertFalse(room.start())
        self.assertNotIn("c", room.ready_set)

    def test_promotion_resets_ready_state(self):
        room = Room(1)
        room.join("a")
        room.join("b")
        room.ready("a")
        room.leave("a")
        self.assertFalse(room.start())
        self.assertNotIn("b", room.ready_set)


class HostTest(unittest.TestCase):
    def test_host_is_lowest_seated_player(self):
        room = Room(3)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("a")
        self.assertEqual(room.host(), "b")

    def test_host_moves_to_next_lowest_seat(self):
        room = Room(3)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("a")
        room.leave("b")
        self.assertEqual(room.host(), "c")

    def test_empty_room_has_no_host(self):
        room = Room(2)
        room.join("a")
        room.leave("a")
        self.assertIsNone(room.host())

    def test_host_after_promotion(self):
        room = Room(2)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("a")
        self.assertEqual(room.host(), "c")


class ScanTest(unittest.TestCase):
    def test_seat_query_is_constant_cost(self):
        room = Room(3000)
        for index in range(3000):
            room.join("p-%d" % index)
        for _ in range(3000):
            room.seat_of_player("p-2999")
        self.assertLessEqual(room.scanned, 3000)

    def test_repeated_sequence_gives_same_result(self):
        def run():
            room = Room(2)
            room.join("a")
            room.join("b")
            room.join("c")
            room.leave("a")
            room.ready("c")
            return room.seat_of_player("c"), room.host(), room.start()
        self.assertEqual(run(), run())


if __name__ == "__main__":
    unittest.main()
