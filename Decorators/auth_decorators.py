
from fastapi import HTTPException, Request, status
from Security.Acls.Permissions import Permissions
from Security.Acls.RoleChecker import Role_checker
from functools import wraps
from fastapi.encoders import jsonable_encoder

from schemas.UserSchema import PermissionSchema, UserSchema

roles_checker = Role_checker()

def requires_vendor_access(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        user = kwargs['user']
        if not roles_checker.vendors_access(user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden"
            )
        return await func(request, *args, **kwargs)
    return wrapper

def requires_permission(permission_type, model_name):
    def decorator(func):
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            user = kwargs.get('user')
            # temp = [PermissionSchema(**jsonable_encoder(p)) for p in user.permissions]
            user = UserSchema(**jsonable_encoder(user))
            # user.permissions = temp   
            print(user)
            permissions = Permissions(user)
            has_permission = getattr(permissions, f'has_{permission_type}_permission')(model_name)
            if not has_permission:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator