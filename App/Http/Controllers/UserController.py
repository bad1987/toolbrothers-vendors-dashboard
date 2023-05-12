from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from rich.console import Console
from App.input_ports.schemas.UserSchema import PermissionSchema, UserCreateSubVendorSchema, UserSchema

from App.output_ports.db.Connexion import SessionLocal
from App.output_ports.models.Models import Permission, User

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
    
    def get_sub_vendor_for_vendor(db_local: Session, request: Request, user: User):
        user_vendor = db_local.query(User).filter(User.parent_id == user.id).all()

        user_permissions = [{"text": permission.name, "value": permission.id, "description": permission.description} for permission in user.permissions]

        return {"users": user_vendor, "permissions": user_permissions}
    
    def create_sub_vendor_by_vendor(request: Request, schema: UserCreateSubVendorSchema, db_local: Session, user_vendor: UserSchema):
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
                
        db_local.commit()
        
        return {"user": userSubVendor} 