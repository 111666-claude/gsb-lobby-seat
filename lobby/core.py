"""房间座位：入座、离开补位、准备状态、开局判定与房主转移。"""

from collections import deque
from heapq import heappop, heappush


class Room:
    """一个固定座位数的房间。"""

    def __init__(self, seats):
        self.seats = seats
        self.seat_of = {}
        self.player_at = [None] * seats
        self.free_seats = list(range(seats))
        self.ready_set = set()
        self.waiting = deque()
        self.scanned = 0

    def join(self, player):
        """入座或排队，返回座位号；排队返回 None。"""
        if player in self.seat_of:
            return self.seat_of.get(player)
        if player in self.waiting:
            return None
        if not self.free_seats:
            self.waiting.append(player)
            return None
        seat = heappop(self.free_seats)
        self.seat_of[player] = seat
        self.player_at[seat] = player
        return seat

    def leave(self, player):
        """离开房间。"""
        if player in self.waiting:
            self.waiting.remove(player)
            return True
        seat = self.seat_of.pop(player, None)
        if seat is None:
            return False
        self.player_at[seat] = None
        self.ready_set.discard(player)
        if self.waiting:
            promoted = self.waiting.popleft()
            self.seat_of[promoted] = seat
            self.player_at[seat] = promoted
            self.ready_set.discard(promoted)
        else:
            heappush(self.free_seats, seat)
        return True

    def ready(self, player, value=True):
        """设置准备状态。"""
        if player not in self.seat_of:
            return False
        if value:
            self.ready_set.add(player)
        else:
            self.ready_set.discard(player)
        return True

    def start(self):
        """开局判定。"""
        return (len(self.seat_of) == self.seats
                and len(self.ready_set) == self.seats)

    def host(self):
        """当前房主。"""
        if not self.seat_of:
            return None
        seat = min(self.seat_of.values())
        return self.player_at[seat]

    def seat_of_player(self, player):
        """玩家所在座位。"""
        self.scanned += 1
        return self.seat_of.get(player)

    def waiting_list(self):
        return list(self.waiting)
