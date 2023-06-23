from enum import Enum

class VarTypeEnum(Enum):
    INT = 'int'
    FLOAT = 'float'
    STRING = 'string'
    BOOL = 'bool'

    @classmethod
    def is_valid_type(cls, type_str):
        for member in cls:
            if type_str == member.value:
                return True
        return False