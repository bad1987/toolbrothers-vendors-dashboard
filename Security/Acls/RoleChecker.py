
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from Database.Models import User
from Security.Controllers.LoginController import get_current_user_from_cookie

class Role_checker:
    def __init__(self, allowed_roles: list) -> None:
        self.allowed_roles = allowed_roles
    
    def __call__(self, request: Request, db: Session):
        user = get_current_user_from_cookie(request, db)
        if (not user) or (user.roles not in self.allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return user
    
    def setRoles(self, roles):
        if isinstance(roles, list):
            for r in roles:
                if r not in self.allowed_roles:
                    self.allowed_roles.append(r)
