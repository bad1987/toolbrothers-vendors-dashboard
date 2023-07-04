from pydantic import BaseModel
from typing import Text, List, Optional
from App.Enums.SystemEnum import VarTypeEnum

class PlatformTypeSchema(BaseModel):
    name: str
    type: VarTypeEnum

class PlatformSimpleSchema(BaseModel):
    id: int
    name: str
    language: str

class PlatformSchemaOut(BaseModel):
    id: Optional[int]
    name: str
    fields: Optional[List[PlatformTypeSchema]]
    status: Optional[bool]
    language: Optional[str]

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

## Admin platform schema

class AdminPlatformSchema(BaseModel):
    id: Optional[int]
    name: str
    fields: Optional[List[PlatformTypeSchema]]
    status: Optional[bool]
    language: str

class AdminPlatformListSchema(BaseModel):
    platforms: List[AdminPlatformSchema]
    languages: List[str]

## User Platform schema
