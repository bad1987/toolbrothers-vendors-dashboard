
from typing import List
from fastapi import HTTPException, Request, status
from App.core.auth.Acls.ModelPermissions import ModelPermissions
from App.core.auth.LoginController import get_current_user_from_cookie

from App.input_ports.schemas.UserSchema import PermissionSchema, UserSchema
from App.output_ports.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session


class UserUsecase:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.db = db

    def get_users_by_type(self, request: Request, type: str) -> List[UserSchema]:
        _user = get_current_user_from_cookie(request=request, db=self.db)
        model_permissions = ModelPermissions(_user)
        if type == "vendors" and model_permissions.can_read_user_vendors():
            return self.user_repository.get_vendors(_user.id)
        elif type == "admins" and model_permissions.can_read_user_admins():
            return self.user_repository.get_admins(_user.id)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden"
            )

    def get_permissions(self) -> List[PermissionSchema]:
        return self.user_repository.get_permissions()
    
    def get_user(self, request: Request):
        _user = get_current_user_from_cookie(request=request, db=self.db)
        return _user