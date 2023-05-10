from enum import Enum

class OrderStatus(str, Enum):
    PROCESSED = "P"
    COMPLETE = "C"
    OPEN = "O"
    FAILED = "F"
    DECLINED = "D"
    BACKORDERED = "B"
    CANCELLED = "I"
    AWAITING_CALL = "Y"