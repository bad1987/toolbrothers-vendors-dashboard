from fastapi import HTTPException, status
from App.Http.Controllers.UserController import UserController
from schemas.UserSchema import PermissionSchema, UserSchema


class Permissions:
    def __init__(self, user:UserSchema):
        self.user = user
        self.userController = UserController()
        self.permissions = []
    def has_read_permission(self, model_name: str):
        # Check if user has read permission for the specified model
        # Return True if user has permission, False otherwise
        self.permissions = self.userController.getPermissions('R', model_name.lower().strip())
        if self.permissions and model_name=='user':
            self.permissions = admin_or_vendor_alc_user(self.permissions, self.user)
        return is_auth(self.permissions, self.user.permissions)
        

    def has_write_permission(self, model_name):
        # Check if user has write permission for the specified model
        # Return True if user has permission, False otherwise
        self.permissions = self.userController.getPermissions('W', model_name.lower().strip())
        if self.permissions and model_name=='user':
            self.permissions = admin_or_vendor_alc_user(self.permissions, self.user)
        return is_auth(self.permissions, self.user.permissions)

    def has_delete_permission(self, model_name):
        # Check if user has delete permission for the specified model
        # Return True if user has permission, False otherwise
        self.permissions = self.userController.getPermissions('D', model_name.lower().strip())
        if self.permissions and model_name=='user':
            self.permissions = admin_or_vendor_alc_user(self.permissions, self.user)
        return is_auth(self.permissions, self.user.permissions)

def is_auth(permissions: list, user_permissions: list[PermissionSchema]):
    if permissions == None or not len(permissions):
            print('No permissions found')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error"
            )
    user_permissions = [p.name for p in user_permissions]
    permissions = permissions[0]
    return permissions in user_permissions


def admin_or_vendor_alc_user(permissions: list[PermissionSchema], user: UserSchema):
    pattern = 'Acl_admin' if user.roles == 'Role_admin' else 'Acl_vendor'
    permissions = [p for p in permissions if p.name.startswith(pattern)]

    return permissions