from enum import IntEnum


class VoteType(IntEnum):
    YEA = 1
    NAY = 2

    @classmethod
    def label(cls, value):
        return {
            cls.YEA: "Yea",
            cls.NAY: "Nay",
        }.get(cls(value), str(value))
