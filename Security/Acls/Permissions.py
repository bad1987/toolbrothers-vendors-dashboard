from fastapi import HTTPException, status
from App.Http.Controllers.UserController import UserController
from schemas.UserSchema import PermissionSchema, UserSchema


class Permissions:
    def __init__(self, user:UserSchema):
        self.user = user
        self.userController = UserController()
        self.permissions = self.userController.getPermissions()
    def has_read_permission(self, model_name: str):
        # Check if user has read permission for the specified model
        # Return True if user has permission, False otherwise
        print(self.user)
        return is_auth(self.permissions, model_name, 'read', self.user.permissions)
        

    def has_write_permission(self, model_name):
        # Check if user has write permission for the specified model
        # Return True if user has permission, False otherwise
        return is_auth(self.permissions, model_name, 'write', self.user.permissions)

    def has_delete_permission(self, model_name):
        # Check if user has delete permission for the specified model
        # Return True if user has permission, False otherwise
        return is_auth(self.permissions, model_name, 'delete', self.user.permissions)

def is_auth(permissions: list, model_name: str, permission_mode: str, user_permissions: list):
    if permissions == None or not len(permissions):
            print('No permissions found')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error"
            )
    model_name = model_name.lower().strip()
    permission = filter_permission(permission_mode, permissions, model_name)
    if not permission:
        return False
    return permission in user_permissions

def filter_permission(mode:str, permissions: list[PermissionSchema], model_name: str):
    mode = mode.lower().strip()
    startwidth = get_pattern(model_name)
    startwidth = startwidth.lower().strip()
    for p in permissions:
        temp = str(p.name.lower())
        temp.strip()
        if temp.endswith(mode):
            if temp.startswith(startwidth):
                return p.name       
    return None

def get_pattern(model_name: str):
    model_name = model_name.lower().strip()
    if model_name == 'products':
        return 'acl_prod'
    if model_name == 'orders':
        return 'acl_ord'
    if model_name == 'vendor':
        return 'acl_vend'
    if model_name == 'admin':
        return 'acl_adm'
    if model_name == 'settings':
        return 'acl_set'