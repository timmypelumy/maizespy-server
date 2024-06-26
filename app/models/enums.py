from enum import StrEnum, unique


@unique
class LabelClasses(StrEnum):
    BLIGHT = "BLIGHT"
    SPOT = "SPOT"
    RUST = "RUST"
    HEALTHY = "HEALTHY"