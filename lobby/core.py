"""房间座位：入座、离开补位、准备状态、开局判定与房主转移。

缺陷：座位号只增不复用、离开后不补位、准备状态不随换座重置、房主取最后一个入座的人、
开局只看人数不看准备、座位查询每次扫全表。
"""


class Room:
    """一个固定座位数的房间。"""

    def __init__(self, seats):
        self.seats = seats
        self.next_seat = 0
        self.seat_of = {}
        self.players = []
        self.ready_set = set()
        self.waiting = []
        self.scanned = 0

    def join(self, player):
        """入座或排队，返回座位号；排队返回 None。"""
        if player in self.seat_of or player in self.waiting:
            return self.seat_of.get(player)
        if len(self.players) >= self.seats:
            self.waiting.append(player)
            return None
        seat = self.next_seat
        self.next_seat += 1
        self.seat_of[player] = seat
        self.players.append(player)
        return seat

    def leave(self, player):
        """离开房间。"""
        if player not in self.seat_of:
            return False
        del self.seat_of[player]
        self.players.remove(player)
        self.ready_set.discard(player)
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
        return len(self.players) >= self.seats

    def host(self):
        """当前房主。"""
        if not self.players:
            return None
        return self.players[-1]

    def seat_of_player(self, player):
        """玩家所在座位。"""
        self.scanned += len(self.seat_of)
        return self.seat_of.get(player)

    def waiting_list(self):
        return list(self.waiting)
