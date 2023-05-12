
import random
import string
from typing import List
from fastapi import HTTPException, status

from sqlalchemy import and_
from App.Enums.LanguageEnum import LanguageEnum
from App.Enums.UserRoleEnum import UserRoleEnum
from App.Http.Schema.UserSchema import UserCreateResponse, UserSchema
from App.core.entities.user_repository import IUserRepository
from sqlalchemy.orm import Session
from App.input_ports.schemas.UserSchema import PermissionSchema, UserCreateSchema


from App.input_ports.schemas.UserSchema import PermissionSchema, UserSchema
from App.output_ports.models.Models import Permission, User
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

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
        return result

    def get_permissions(self) -> List[PermissionSchema]:
        permissions = self.db.query(Permission).all()
        # permissions = [PermissionSchema(**{"text": perm.name, "value": perm.id, "description": perm.description}) for perm in permissions]
        return permissions
    
    def create_user(self, model: UserCreateSchema) -> UserCreateResponse:
        user = User()
        pwd_pattern = string.ascii_letters + string.digits + "@#$%^&*()./+-!"
        pwd = ''.join(random.choices(pwd_pattern, k = random.randrange(8, 18)))

        user.username = model.username
        user.email = model.email
        user.password = crypto.hash(pwd) # TODO: Create a random password and send mail
        user.status = model.status.value
        user.roles = model.roles.value
        user.default_language = LanguageEnum.DE.value

        self.db.add(user)

        permission_ids = [int(perm_id) for perm_id in model.permissions]
        permissions = self.db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        user.permissions.extend(permissions)

        self.db.commit()

        return {"user": UserSchema.from_orm(user), "password": pwd}
    
    def update_user(self, id: int, model: UserSchema) -> UserSchema:
        user_to_update = self.db.query(User).filter(User.id == id).first()

        if not user_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found"
            )
        
        for field, value in model.dict(exclude_unset=True, exclude={'permissions'}).items():
            setattr(user_to_update, field, value)

        if model.permissions != None:
            user_to_update.permissions.clear()

            permission_ids = [int(perm_id) for perm_id in model.permissions]
            permissions = self.db.query(Permission).filter(Permission.id.in_(permission_ids)).all()

            user_to_update.permissions.extend(permissions)
                
        self.db.commit()
        self.db.refresh(user_to_update)

        return user_to_update