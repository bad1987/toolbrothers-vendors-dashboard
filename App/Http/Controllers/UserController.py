
from Database.Connexion import SessionLocal
from Database.Models import Permission, User_Permission
from schemas.UserSchema import PermissionSchema
from fastapi.encoders import jsonable_encoder

class UserController:

    def getPermissions(self, mode: str, model_name: str):
        permissions = []
        try:
            db = SessionLocal()
            permissions = db.query(Permission).filter(Permission.mode == mode).filter(Permission.model_name == model_name).all()
            for p in permissions:
                permissions.append(PermissionSchema(**jsonable_encoder(p)))
        except Exception as e:
            print(str(e))
            permissions = None
        finally:
            db.close()
        
        return permissions