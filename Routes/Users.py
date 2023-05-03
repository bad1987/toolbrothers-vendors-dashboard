import re
from typing import List, Any, Dict
from fastapi import Depends, HTTPException,Request, APIRouter, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
from Decorators.auth_decorators import requires_permission
from Security.Acls.ModelPermissions import ModelPermissions
from Security.Acls.RoleChecker import Role_checker
from Security.Controllers import LoginController
from Security.DTO.UserDto import UserDtoCreate, UserDto, UserListDto, Permission
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from sqlalchemy import or_
from Database.Models import User, Payment_method, Payment_method_vendor, User_Permission, Permission
from rich.console import Console
from fastapi.encoders import jsonable_encoder
from Database.CscartModels import CscartCompanies, Cscart_payments
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from App.Enums.UserRoleEnum import ModelNameEnum, UserRoleEnum
from App.Enums.LanguageEnum import LanguageEnum
from Services.SendEmail import send_email
import traceback, sys, random, string

from App.Http.Schema.UserSchema import UserSchema

console = Console()

route = APIRouter(prefix='/admin', tags=['Users system'])

roles_checker = Role_checker()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#Connexion from cscart database

def get_db_cscart():
    db_cscart = CscartSession()
    try:
        yield db_cscart
    finally:
        db_cscart.close()


#check if user is connected
async def is_authenticated(request: Request, db: Session = Depends(get_db)):
    user = LoginController.get_current_user_from_cookie(request, db)

    if not user:
        user = LoginController.get_current_user_from_api_token(request, db)

    console.log(user)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    return user


@route.get("/user", response_model=UserSchema)
def get_user(request: Request, db: Session = Depends(get_db)):
    user = LoginController.get_current_user_from_cookie(request, db)

    return user


@route.get("/users/{type}/list", response_model=UserListDto, responses={200:{"model": UserSchema}})#, response_model=list(UserSchema)
@requires_permission('read', ModelNameEnum.USER_MODEL.value)
async def index(request: Request, type: str, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):

    users = []
    model_permissions = ModelPermissions(_user)
    if type == "vendors" and model_permissions.can_read_user_vendors():
        users = db.query(User).filter(or_(User.roles == UserRoleEnum.AFFILIATE.value, User.roles == UserRoleEnum.DIRECT_SALE.value)).all()
    elif type == "admins" and model_permissions.can_read_user_admins():
        users = db.query(User).filter(User.roles == UserRoleEnum.ADMIN.value).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden"
        )

    permissions = db.query(Permission).all()
        
    return {"users": users, "permissions": [{"text": perm.name, "value": perm.id, "description": perm.description} for perm in permissions]}

@route.get('/get-all-users', response_class=JSONResponse)
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    # user = LoginController.get_current_user_from_cookie(request, db)
    # console.log(user)
    users = db.query(User).all()

    datas = []

    return {'users': users}

@route.delete('/users', response_class=JSONResponse)
@requires_permission('delete', ModelNameEnum.USER_MODEL.value)
async def delete_user(request: Request, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    try:
        user = LoginController.get_current_user_from_cookie(request, db)
        datas = await request.json()
        
        return {
            'status': True,
            'message': 'Ok'
        }
    except:
        return {
            'status': False,
            'message': 'An error occured'
        }

@route.post('/users', response_model= UserSchema | Dict[str, str], status_code=201)
@requires_permission('write', ModelNameEnum.USER_MODEL.value)
async def add_user(request: Request, model: UserDtoCreate, response: Response, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    resolved = None
    is_resolved = False
    try:
        if db.in_transaction():
            db.rollback()
        with db.begin():
            # transaction = db.begin()
            # console.log(transaction)
            user = User()
            pwd_pattern = string.ascii_letters + string.digits + "@#$%^&*()./+-!"
            pwd = ''.join(random.choices(pwd_pattern, k = random.randrange(8, 18)))

            user.username = model.username
            user.email = model.email
            user.password = crypto.hash(pwd) # TODO: Create a random password and send mail
            user.status = model.status.value
            user.roles = model.roles.value
            user.default_language = LanguageEnum.DE.value

            db.add(user)

            for perm_id in model.permissions:
                permission = db.query(Permission).filter(Permission.id == int(perm_id)).first()

                if permission != None: 
                    user.permissions.append(permission)
                else:
                    continue

            db.commit()

             ## send email to the user
            
            resolved = user
            is_resolved = True
           
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        db.rollback()
        resolved = {'status': False, 'message': str(e)}

    if is_resolved:
        send_email(user.email, 'New account infos', 
                f"""
                    Login to your vendor dashboard
                    Your infos\n\n
                    email: {user.email}\n
                    password: {pwd}\n\n
                """
            )
    return resolved
    

@route.put('/users/{id}', response_model=UserSchema | Dict[str, str])
@requires_permission('write', ModelNameEnum.USER_MODEL.value)
async def update_user(id: int, model: UserSchema, request: Request,  db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    try:
        if db.in_transaction():
            db.rollback()
        transaction = db.begin()
        current_user = is_authenticated(request, db)
        user_to_update = db.query(User).filter(User.id == id).first()

        if not user_to_update:
            return {"status": False, "message": "Invalid user"}
        
        for field, value in model.dict(exclude_unset=True, exclude={'permissions'}).items():
            setattr(user_to_update, field, value)

        if model.permissions != None:
            user_to_update.permissions.clear()

            for perm_id in model.permissions:
                permission = db.query(Permission).filter(Permission.id == int(perm_id)).first()

                if permission != None: 
                    user_to_update.permissions.append(permission)
                else:
                    continue
                
        db.commit()
        db.refresh(user_to_update)

        return user_to_update
    except Exception as e:
        transaction.rollback()
        return { "status": False, "message": str(e) }

# Scrap user vendor in cscart database
@route.get('/cscart-users')
async def cscart_users(db_cscart: Session = Depends(get_db_cscart), db_local: Session = Depends(get_db)):
    
    try:
        companies = db_cscart.query(CscartCompanies).all()
        
        for item in companies:
            is_exist = db_local.query(User).filter(User.email == item.email).first()
            
            if is_exist:
                console.log("This user exist", item.company)    
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
                        result = extract_credentials(item_cscart.processor_params)
                        
                        # Add secret credentials
                        if result:
                            payment_method_vendor_local.client_secret = result['password']
                            payment_method_vendor_local.client_secret_id = result['username']
                            console.log("credential extract", result['username'], result['password'])
                        
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
                    
                        console.log("Method payment for user. Company_id : ", item_cscart.payment_id)
                        continue
                continue
            
            db_local.flush(user)
            
            console.log("Add success", user.username)
        return {'status': True, 'message': 'Finished'}
    except Exception as e:
        console.log("error ...", str(e))
    
@route.get('/users/create-admin-users')
async def create_admin(db_local: Session = Depends(get_db)):
    user = User()

    user.company_id = -1
    user.email = "admin@dino.com"
    user.password = crypto.hash("Admin")
    user.roles = "Role_master_admin"
    user.status = "A"
    user.username = "Admin"

    db_local.add(user)
    db_local.commit()
    db_local.flush(user)

    return None

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

