from pydantic import BaseModel
from typing import Text, List, Optional
from App.Enums.SystemEnum import VarTypeEnum

class PlatformTypeSchema(BaseModel):
    name: str
    type: VarTypeEnum

class PlatformSimpleSchema(BaseModel):
    id: int
    name: str

class PlatformSchemaOut(BaseModel):
    id: Optional[int]
    name: str
    fields: Optional[List[PlatformTypeSchema]]
    status: Optional[bool]

class PlatformFieldValuesSchema(BaseModel):
    name: str
    value: str

class PlatformUserSchema(BaseModel):
    name: str
    values: Optional[List[PlatformFieldValuesSchema]]

## User platform schema

class UserPlatformSchema(BaseModel):
    id: int
    name: Optional[str]
    fields: Optional[List[PlatformTypeSchema]]
    status: Optional[bool]
    values: List[PlatformFieldValuesSchema]

class UserPlatformSchemaIn(BaseModel):
    id: int
    values: List[PlatformFieldValuesSchema]
