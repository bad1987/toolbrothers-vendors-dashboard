
from Database.Connexion import SessionLocal
from Database.Models import Permission, User_Permission
from App.Http.Schema.UserSchema import PermissionSchema
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List

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