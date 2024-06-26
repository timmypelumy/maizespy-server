from enum import StrEnum, unique


@unique
class ResultClasses(StrEnum):
    BLIGHT = "BLIGHT"
    SPOT = "SPOT"
    RUST = "RUST"
    HEALTHY = "HEALTHY"