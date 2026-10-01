"""命令行入口：跑房间座位样例。"""

import argparse

from .core import Room


def build_parser():
    parser = argparse.ArgumentParser(prog="lobby-seat", description="房间座位")
    parser.add_argument("--sample", default="seat",
                        help="seat / queue / start / ready / host / scan")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "seat":
        room = Room(3)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("b")
        seat = room.join("d")
        print("seat=%s" % seat)
    elif args.sample == "queue":
        room = Room(2)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("a")
        print("waiting=%d promoted=%s"
              % (len(room.waiting_list()),
                 str(room.seat_of_player("c") == 0).lower()))
    elif args.sample == "start":
        room = Room(2)
        room.join("a")
        room.join("b")
        room.ready("a")
        print("start=%s" % str(room.start()).lower())
    elif args.sample == "ready":
        room = Room(2)
        room.join("a")
        room.join("b")
        room.ready("a")
        room.ready("b")
        room.leave("b")
        room.join("c")
        print("start=%s ready_c=%s"
              % (str(room.start()).lower(),
                 str(room.ready_set and "c" in room.ready_set).lower()))
    elif args.sample == "host":
        room = Room(3)
        room.join("a")
        room.join("b")
        room.join("c")
        room.leave("a")
        print("host=%s" % room.host())
    elif args.sample == "scan":
        room = Room(3000)
        for index in range(3000):
            room.join("p-%d" % index)
        for _ in range(3000):
            room.seat_of_player("p-2999")
        print("scanned=%d" % room.scanned)
    else:
        raise SystemExit("需要 --sample seat|queue|start|ready|host|scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
