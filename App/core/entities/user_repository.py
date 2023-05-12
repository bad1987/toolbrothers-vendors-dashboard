
from abc import ABC, abstractmethod
from typing import List, Optional

from fastapi import Request
from sqlalchemy.orm import Session
from App.Http.Schema.UserSchema import UserCreateResponse

from App.input_ports.schemas.UserSchema import PermissionSchema, UserCreateSchema, UserSchema

class IUserRepository(ABC):
    
    def get_vendors(self, user_id: int) -> List[UserSchema]:
        ...

    def get_admins(self, user_id: int) -> List[UserSchema]:
        ...

    def get_permissions(self) -> List[PermissionSchema]:
        ...
    
    def create_user(self, model: UserCreateSchema) -> UserCreateResponse:
        ...
    
    def update_user(self, id:int, model: UserSchema) -> UserSchema:
        ...