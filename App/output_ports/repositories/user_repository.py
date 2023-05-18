
from datetime import datetime, timedelta
import random, string, re
from typing import List, Optional
from fastapi import HTTPException, status
import jwt

from sqlalchemy import and_
from App.Enums.LanguageEnum import LanguageEnum
from App.Enums.UserRoleEnum import UserRoleEnum
from App.Http.Schema.UserSchema import UserCreateResponse, UserSchema
from App.core.auth.Configs.Settings import Settings
from App.core.entities.user_repository import IUserRepository
from sqlalchemy.orm import Session
from App.input_ports.schemas.UserSchema import PermissionSchema, UserCreateSchema


from App.input_ports.schemas.UserSchema import PermissionSchema, UserSchema
from App.output_ports.models.CscartModels import Cscart_payments, CscartCompanies
from App.output_ports.models.Models import Payment_method, Payment_method_vendor, Permission, User
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

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
        result = [UserSchema.from_orm(p) for p in result]
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

    def get_permissions(self) -> List[PermissionSchema]:
        permissions = self.db.query(Permission).all()
        # permissions = [PermissionSchema(**{"text": perm.name, "value": perm.id, "description": perm.description}) for perm in permissions]
        return permissions
    
    def create_user(self, model: UserCreateSchema) -> UserCreateResponse:
        user = User()
        pwd_pattern = string.ascii_letters + string.digits + "@#$%^&*()./+-!"
        pwd = ''.join(random.choices(pwd_pattern, k = random.randrange(8, 18)))

        user.username = model.username
        user.email = model.email
        user.password = crypto.hash(pwd) # TODO: Create a random password and send mail
        user.status = model.status.value
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
        
        for field, value in model.dict(exclude_unset=True, exclude={'permissions'}).items():
            setattr(user_to_update, field, value)

        if model.permissions != None:
            user_to_update.permissions.clear()

            permission_ids = [int(perm_id) for perm_id in model.permissions]
            permissions = self.db.query(Permission).filter(Permission.id.in_(permission_ids)).all()

            user_to_update.permissions.extend(permissions)
                
        self.db.commit()
        self.db.refresh(user_to_update)

        return user_to_update

    def import_cscart_users(self, db_cscart: Session, db_local: Session) -> List[UserSchema]:
        companies = db_cscart.query(CscartCompanies).all()
        
        for item in companies:
            is_exist = db_local.query(User).filter(User.email == item.email).first()
            
            if is_exist:
                continue
            
            user = User()
            
            user.company_id = item.company_id
            user.username = item.company
            user.email = item.email
            user.password = crypto.hash(f"{item.email}".split("@")[0]+"@!"+str(item.company_id))
            user.roles = "Role_direct_sale" if (item.company_id == 4 or item.company_id ==205) else "Role_affiliate"
            user.status = item.status
            
            db_local.add(user) 
            db_local.commit() 
            
            payment_method_vendor = db_cscart.query(Cscart_payments).filter(Cscart_payments.company_id == item.company_id).all()
            if payment_method_vendor:
                
                for item_cscart in payment_method_vendor:
                    payment_method_vendor_local = Payment_method_vendor()
                    method_vendor = db_local.query(Payment_method).filter(Payment_method.processor_id == item_cscart.processor_id).first()
                    
                    if method_vendor:
                        result = self.extract_credentials(item_cscart.processor_params)
                        
                        # Add secret credentials
                        if result:
                            payment_method_vendor_local.client_secret = result['password']
                            payment_method_vendor_local.client_secret_id = result['username']
                        
                        payment_method_vendor_local.payment_id = user.company_id
                        payment_method_vendor_local.name = method_vendor.name
                        payment_method_vendor_local.processor_params = item_cscart.processor_params
                        payment_method_vendor_local.status = item_cscart.status
                        payment_method_vendor_local.user_id = user.id
                        payment_method_vendor_local.processor_id = method_vendor.processor_id
                        payment_method_vendor_local.payment_method_id = method_vendor.id
                        
                        db_local.add(payment_method_vendor_local)
                        db_local.commit()
                        db_local.flush(payment_method_vendor)
                    
                        continue
                continue
            
            db_local.flush(user)
            
        return {'status': True, 'message': 'Finished'}


    # Extract secret credential
    def extract_credentials(payload: str):
        if not payload:
            return None
        regex = '^.*?"username".*?"(.*?)".*?"password".*?"(.*?)"'
        res = re.findall(regex, payload)
        if len(res) and isinstance(res[0], tuple):
            return {
                'username': res[0][0],
                'password': res[0][1],
            }
        regex = '^.*?"client_id".*?"(.*?)".*?"secret".*?"(.*?)"'
        res = re.findall(regex, payload)
        if len(res) and isinstance(res[0], tuple):
            return {
                'username': res[0][0],
                'password': res[0][1],
            }
        return None