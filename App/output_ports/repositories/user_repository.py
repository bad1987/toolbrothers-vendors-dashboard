
from datetime import datetime, timedelta
import random, string, re
from typing import List, Optional
from fastapi import HTTPException, status
import jwt, json

from sqlalchemy import and_
from App.Enums.LanguageEnum import LanguageEnum
from App.Enums.UserEnums import UserStatusEnum
from App.Enums.UserRoleEnum import UserRoleEnum
from App.Http.Schema.PlatformSchema import PlatformSimpleSchema
from App.Http.Schema.UserSchema import UserCreateResponse, UserSchema
from App.core.auth.Configs.Settings import Settings
from App.core.entities.user_repository import IUserRepository
from sqlalchemy.orm import Session
from App.input_ports.schemas.UserSchema import PermissionSchema, UserCreateSchema
from App.input_ports.schemas.UserSchema import PermissionSchema, UserSchema
from App.output_ports.models.CscartModels import Cscart_payments, CscartCompanies
from App.output_ports.models.Models import Payment_method, Payment_method_vendor, Permission, Platform, Platform_Data, Platform_settings, User, User_Permission, User_Platform
from passlib.handlers.sha2_crypt import sha512_crypt as crypto


from rich.console import Console

console = Console()

class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_vendors(self, user_id: int) -> List[UserSchema]:
        result = self.db.query(User).filter(
            and_(
                User.roles != UserRoleEnum.ADMIN.value,
                User.parent_id == None,
                User.id != user_id,
            )
        ).all()
        result = [UserSchema.from_user(p) for p in result]
        return result

    def get_platform_simple_list(self) -> List[PlatformSimpleSchema]:
        result = self.db.query(Platform_Data).all()
        result = [PlatformSimpleSchema(**{'id': p.platform_id, 'name': p.name, 'language': p.language}) for p in result]

        return result

    def get_admins(self, user_id: int) -> List[UserSchema]:
        result = self.db.query(User).filter(
            and_(User.roles == UserRoleEnum.ADMIN.value, User.id != user_id)
        ).all()
        result = [UserSchema.from_orm(p) for p in result]
        return result
    
    def get_user(self, username:str = None, email: str = None) -> Optional[UserSchema]:
        if username:
            user = self.db.query(User).filter(User.username == username).first()
        elif email:
            user = self.db.query(User).filter(User.email == email).first()
        return user

    def get_user_by_id(self, id: int) -> Optional[UserSchema]:
        user = self.db.query(User).filter(User.id == id).first()
        return user
    
    def get_parent(self, parent_id: int) -> UserSchema:
        parent = self.db.query(User).filter(User.id == parent_id).first()
        return UserSchema.from_user(parent)
    
    def generate_api_token(self, email: str):
        userToken: User = self.get_user(email=email)
        if userToken is None:
            return None
        
        
        expire_time = datetime.utcnow() + timedelta(days=Settings.API_TOKEN_EXPIRE_DAYS)
        playload = {"exp": expire_time, "email": userToken.email}
        encoded_token = jwt.encode(playload, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
        
        userToken.api_token = encoded_token
        self.db.commit()

        return encoded_token

    def update_password(self, new_hashed_password: str, email: str) -> User:
        user: User = self.get_user(email=email)
        if user:
            user.password = new_hashed_password
            self.db.commit()
            self.db.flush(user)
        return user
    
    def get_permissions(self) -> List[PermissionSchema]:
        permissions = self.db.query(Permission).all()
        # permissions = [PermissionSchema(**{"text": perm.name, "value": perm.id, "description": perm.description}) for perm in permissions]
        return permissions
    
    def create_user(self, model: UserCreateSchema) -> UserCreateResponse:
        user = User()
        pwd_pattern = string.ascii_letters + string.digits + "@#$%^&*()./+-!"
        pwd = ''.join(random.choices(pwd_pattern, k = random.randrange(8, 18)))

        # check if email already. if yes, raise a 422 exception
        _user = self.get_user(email=model.email)
        if _user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Email already exists"
            )

        user.username = model.username
        user.email = model.email
        user.password = crypto.hash(pwd) # TODO: Create a random password and send mail
        user.status = UserStatusEnum.PENDING.value # status is pending until the user is assigned a company_id
        user.roles = model.roles.value
        user.default_language = LanguageEnum.DE.value

        self.db.add(user)

        permission_ids = [int(perm_id) for perm_id in model.permissions]
        permissions = self.db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        user.permissions.extend(permissions)

        self.db.commit()

        return {"user": UserSchema.from_orm(user), "password": pwd}
    
    def update_user(self, id: int, model: UserSchema) -> UserSchema:
        user_to_update = self.db.query(User).filter(User.id == id).first()

        if not user_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found"
            )
        
        for field, value in model.dict(exclude_unset=True, exclude={'permissions', "status", "platform"}).items():
            setattr(user_to_update, field, value)

        if (user_to_update.status.value != UserStatusEnum.ACTIVE.value 
            and model.status == UserStatusEnum.ACTIVE
            and user_to_update.company_id is None
            and user_to_update.roles.value != UserRoleEnum.ADMIN.value
            ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This user cannot be activated, unknown company"
            )

        elif model.status: user_to_update.status = model.status.value

        if model.permissions != None:
            user_to_update.permissions.clear()

            permission_ids = [int(perm_id) for perm_id in model.permissions]
            permissions = self.db.query(Permission).filter(Permission.id.in_(permission_ids)).all()

            user_to_update.permissions.extend(permissions)

        if model.platform_id:
            user_platform = self.db.query(User_Platform).filter(and_(User_Platform.user_id == id, User_Platform.platform_id == model.platform_id))

            datas = self.db.query(Platform_Data).filter(Platform_Data.platform_id == model.platform_id).first()
            print(datas)
            values = {}

            for index, key in enumerate(json.loads(datas.fields)):
                values[index] = ''

            if user_platform == None:
                self.db.add(User_Platform(
                    values = json.dumps(values),
                    user_id = user_to_update.id,
                    platform_id = model.platform_id,
                ))
            else:
                user_platform.values = json.dumps(values)

        self.db.commit()
        self.db.refresh(user_to_update)

        return user_to_update
    
    # delete a user by id
    def delete_user(self, id: int) -> bool:
        user = self.db.query(User).filter(User.id == id).first()
        if user:
            self.db.query(User_Permission).filter(User_Permission.id == id).delete()
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def import_cscart_users(self, db_cscart: Session, db_local: Session) -> List[UserSchema]:

        # the import is made inside the method in order to avoid the circular import problem
        from Seeders.seed import add_payment_method, create_permissions, import_vendor
        from Seeders.data import data_payment_method, permission_data

        # Add payment method system
        add_payment_method(data_payment_method, db_local)
        
        # Add permission system
        create_permissions(permission_data, db_local)
        
        # Import user in cscart from db local
        import_vendor(db_local, db_cscart)
            
        return {'status': True, 'message': 'Finished'}
