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
        
        return user_vendor
    
    def create_sub_vendor_by_vendor(request: Request, schema: UserCreateSubVendorSchema, db_local: Session):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        user_vendor = db_local.query(User).filter(User.id == user.id).first()
        userSubVendor = User()
        
        userSubVendor.email = schema.email
        userSubVendor.username = schema.username
        if schema.firstname:
            userSubVendor.firstname = schema.firstname
        if schema.lastname:
            userSubVendor.lastname = schema.lastname
        if schema.default_language:
            userSubVendor.default_language = schema.default_language
        else:
            userSubVendor.default_language = "en"
        userSubVendor.roles = user_vendor.roles
        userSubVendor.status = schema.status
        userSubVendor.parent_id = user_vendor.id
        userSubVendor.password = crypto.hash(f"{schema.password}")
        
        db_local.add(userSubVendor)
        db_local.commit()

        if schema.permissions:
            for perm_id in schema.permissions:
                permission = db_local.query(Permission).filter(Permission.id == int(perm_id)).first()

                if permission != None: 
                    
                    userPermission = User_Permission()
                    
                    userPermission.permission_id = permission.id
                    userPermission.user_id = userSubVendor.id
                    
                    db_local.add(userPermission)
                    db_local.commit()
                    db_local.flush(userPermission)
                
        db_local.flush(userSubVendor)
        
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Create successful !!')   
                