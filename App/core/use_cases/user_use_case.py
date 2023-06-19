
from typing import List
from fastapi import HTTPException, Request, status
from App.core.Services.SendEmail import send_email
from App.core.auth.Acls.ModelPermissions import ModelPermissions
from App.core.auth.LoginController import get_current_user_from_cookie

from App.input_ports.schemas.UserSchema import PermissionSchema, UserCreateSchema, UserSchema
from App.output_ports.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()
site_url = os.getenv("SERVER_HOST")


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
        try:
            return self.user_repository.get_permissions()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    def get_user(self, request: Request):
        _user = get_current_user_from_cookie(request=request, db=self.db)
        return _user
    
    def create_user(self, model: UserCreateSchema) -> UserSchema:
        resolved = None
        try:
            resolved = self.user_repository.create_user(model)
            send_email(resolved['user'].email, 'New account infos', 
                f"""
                    Login to your vendor dashboard at {site_url}\n
                    Your infos\n\n
                    email: {resolved['user'].email}\n
                    password: {resolved['password']}\n\n
                """
            )
        except Exception as e:
            # if it is a 422 code, raise as it is
            if isinstance(e, HTTPException) and e.status_code == 422:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= str(e)
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= str(e)
            )
        return resolved['user']
    
    def update_user(self, id: int, model: UserCreateSchema) -> UserSchema:
        try:
            user = self.user_repository.update_user(model=model, id=id)
            return user
        except Exception as e:
            if isinstance(e, HTTPException) and e.status_code == 404:
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= str(e)
            )
    
    def delete_user(self, id: int) -> dict:
        try:
            res:bool = self.user_repository.delete_user(id=id)
            message = "User deleted successfully" if res else "Failed to delete user"
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail= message
                )
            return {'message': message}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def import_cscart_users(self, db_cscart: Session, db_local: Session) -> List[UserSchema]:
        try:
            result = self.user_repository.import_cscart_users(db_cscart, db_local)
            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= str(e)
            )