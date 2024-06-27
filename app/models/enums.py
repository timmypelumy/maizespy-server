from enum import Enum, unique


@unique
class LabelClasses( str,Enum):
    BLIGHT = "BLIGHT"
    SPOT = "SPOT"
    RUST = "RUST"
    HEALTHY = "HEALTHY"