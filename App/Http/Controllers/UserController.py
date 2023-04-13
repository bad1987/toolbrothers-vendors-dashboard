
from Database.Connexion import SessionLocal
from Database.Models import User_Permission
from schemas.UserSchema import PermissionSchema
from fastapi.encoders import jsonable_encoder

class UserController:

    def getPermissions(self):
        permissions = []
        try:
            db = SessionLocal()
            permissions = db.query(User_Permission).all()
            for p in permissions:
                permissions.append(PermissionSchema(**jsonable_encoder(p)))
        except Exception as e:
            print(str(e))
            permissions = None
        finally:
            db.close()
        
        return permissions