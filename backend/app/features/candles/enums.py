from enum import StrEnum


class Timeframe(StrEnum):
    minute_1 = "MINUTE_1"
    minute_5 = "MINUTE_5"
    minute_15 = "MINUTE_15"
    minute_60 = "MINUTE_60"
    minute_240 = "MINUTE_240"
    day = "DAY"
