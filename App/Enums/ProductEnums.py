from enum import Enum

class ProductStatus(str, Enum):
    ACTIVE = "A"
    HIDDEN = "H"
    DISABLED = "D"