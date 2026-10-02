"""房间座位：入座、离开补位、准备状态、开局判定与房主转移。

座位分配占用编号最小的空座；座位满了进等待队列，有人离开时队首立刻补进
释放的座位；离开或补位都会重置准备状态；所有座位有人且全部准备才能开局；
房主是座位号最小的在场玩家；座位查询 O(1)。
"""

import heapq
from collections import deque


class Room:
    """一个固定座位数的房间。"""

    def __init__(self, seats):
        self.seats = seats
        self.seat_of = {}
        self.player_at = {}
        self.ready_set = set()
        self.waiting = deque()
        self.waiting_set = set()
        self.scanned = 0
        self._next_seat = 0
        self._free_seats = []
        self._occupied = []

    def join(self, player):
        """入座或排队，返回座位号；排队返回 None。"""
        if player in self.seat_of:
            return self.seat_of[player]
        if player in self.waiting_set:
            return None
        seat = self._alloc_seat()
        if seat is None:
            self.waiting.append(player)
            self.waiting_set.add(player)
            return None
        self._occupy(player, seat)
        return seat

    def leave(self, player):
        """离开房间；有人等待时队首立刻补进释放的座位。"""
        if player not in self.seat_of:
            return False
        seat = self.seat_of.pop(player)
        del self.player_at[seat]
        self.ready_set.discard(player)
        if self.waiting:
            promoted = self.waiting.popleft()
            self.waiting_set.discard(promoted)
            self.ready_set.discard(promoted)
            self._occupy(promoted, seat)
        else:
            heapq.heappush(self._free_seats, seat)
        return True

    def ready(self, player, value=True):
        """设置准备状态，只有已入座的人可以准备。"""
        if player not in self.seat_of:
            return False
        if value:
            self.ready_set.add(player)
        else:
            self.ready_set.discard(player)
        return True

    def start(self):
        """所有座位有人且在场玩家全部准备才返回 True，否则 False。"""
        return (len(self.seat_of) == self.seats
                and len(self.ready_set) == len(self.seat_of))

    def host(self):
        """房主是座位号最小的在场玩家；房间空时没有房主。"""
        while self._occupied:
            seat, player = self._occupied[0]
            if self.player_at.get(seat) == player:
                return player
            heapq.heappop(self._occupied)
        return None

    def seat_of_player(self, player):
        """玩家所在座位，O(1) 查询。"""
        self.scanned += 1
        return self.seat_of.get(player)

    def waiting_list(self):
        return list(self.waiting)

    def _alloc_seat(self):
        """分配编号最小的空座；没有空座返回 None。"""
        if self._free_seats:
            return heapq.heappop(self._free_seats)
        if self._next_seat < self.seats:
            seat = self._next_seat
            self._next_seat += 1
            return seat
        return None

    def _occupy(self, player, seat):
        self.seat_of[player] = seat
        self.player_at[seat] = player
        heapq.heappush(self._occupied, (seat, player))
