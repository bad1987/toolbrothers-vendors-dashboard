
from typing import List

from sqlalchemy import and_
from App.Enums.UserRoleEnum import UserRoleEnum
from App.Http.Schema.UserSchema import UserSchema
from App.core.entities.user_repository import IUserRepository
from sqlalchemy.orm import Session
from App.input_ports.schemas.UserSchema import PermissionSchema


from App.input_ports.schemas.UserSchema import PermissionSchema, UserSchema
from App.output_ports.models.Models import Permission, User

class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_vendors(self, user_id: int) -> List[UserSchema]:
        result = self.db.query(User).filter(
            and_(
                User.roles != UserRoleEnum.ADMIN.value,
                User.parent_id == None,
                User.id != user_id,
            )
        ).all()
        result = [UserSchema.from_orm(p) for p in result]
        return result

    def get_admins(self, user_id: int) -> List[UserSchema]:
        result = self.db.query(User).filter(
            and_(User.roles == UserRoleEnum.ADMIN.value, User.id != user_id)
        ).all()
        result = [UserSchema.from_orm(p) for p in result]

    def get_permissions(self) -> List[PermissionSchema]:
        permissions = self.db.query(Permission).all()
        permissions = [PermissionSchema({"text": perm.name, "value": perm.id, "description": perm.description}) for perm in permissions]
        return permissions