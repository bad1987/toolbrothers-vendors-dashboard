
from fastapi import HTTPException, Request, status
from Security.Acls.Permissions import PermissionChecker
from Security.Acls.RoleChecker import Role_checker
from functools import wraps

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

# def requires_permission(permission_type, model_name):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(request, *args, **kwargs):
#             user = kwargs.get('_user')
#             permissions = PermissionChecker(user)
#             has_permission = getattr(permissions, f'has_{permission_type}_permission')(model_name)
#             if not has_permission:
#                 raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")
#             # if 'type' in kwargs:
#             #     kwargs.pop('type')
#             return await func(request, *args, **kwargs)
#         return wrapper
#     return decorator

def requires_permission(permission_type: str, model_name: str):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            user = kwargs.get('_user')  # get the user object from the first argument
            print(f'user object: {user}')
            if not user or not hasattr(user, 'roles') or not hasattr(user, 'id'):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

            # check if the user has the required permission for the model
            permission_checker = PermissionChecker(user)
            has_permission = getattr(permission_checker, f'has_{permission_type}_permission')(model_name)
            if not has_permission:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')

            return await func(*args, **kwargs)

        return wrapped

    return wrapper
