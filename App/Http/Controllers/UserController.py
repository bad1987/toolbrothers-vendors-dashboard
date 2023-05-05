from fastapi import Request, status
from Database.Connexion import SessionLocal
from Database.Models import Permission, User, User_Permission
from App.Http.Schema.UserSchema import PermissionSchema
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from Security.Controllers import LoginController
from App.Http.Schema.UserSchema import UserCreateSubVendorSchema
from typing import List
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from fastapi.responses import JSONResponse
from rich.console import Console

from Security.DTO.UserDto import UserDto

console = Console()


class UserController:

    def getPermissions(self, mode: str, model_name: str) -> List[PermissionSchema]:
        try:
            db: Session = SessionLocal()
            permissions: List[Permission] = db.query(Permission).filter(Permission.mode == mode, Permission.model_name == model_name).all()
            permission_schemas: List[PermissionSchema] = [PermissionSchema(**jsonable_encoder(p)) for p in permissions]
        except Exception as e:
            print(str(e))
            permission_schemas = None
        finally:
            db.close()
        return permission_schemas
    
    def get_sub_vendor_for_vendor(db_local: Session, request: Request):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        
        user_vendor = db_local.query(User).filter(User.parent_id == user.id).all()
        permissions = db_local.query(Permission).all()
        
        return {"users": user_vendor, "permissions": permissions}
    
    def create_sub_vendor_by_vendor(request: Request, schema: UserCreateSubVendorSchema, db_local: Session, user_vendor: UserDto):
        userSubVendor = User()
        
        userSubVendor.email = schema.email
        userSubVendor.username = schema.username
        userSubVendor.firstname = schema.firstname
        userSubVendor.lastname = schema.lastname
        userSubVendor.default_language = user_vendor.default_language
        userSubVendor.roles = user_vendor.roles
        userSubVendor.status = schema.status
        userSubVendor.parent_id = user_vendor.id
        userSubVendor.password = crypto.hash(f"{schema.password}")
        
        db_local.add(userSubVendor)

        if schema.permissions:
            for perm_id in schema.permissions:
                permission = db_local.query(Permission).filter(Permission.id == int(perm_id)).first()

                if permission != None: 
                    userSubVendor.permissions.append(permission)
                
        db_local.commit(userSubVendor)
        
        return {"user": userSubVendor} 
                