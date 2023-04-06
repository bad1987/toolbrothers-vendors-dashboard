import re
from typing import List
from fastapi import Depends, HTTPException,Request, APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from Security.Acls.RoleChecker import Role_checker
from Security.Controllers import LoginController
from Security.DTO.UserDto import UserDtoCreate, UserDto, AdminDtoCreate
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from sqlalchemy import or_
from Database.Models import User, Payment_method, Payment_method_vendor
from rich.console import Console
from fastapi.encoders import jsonable_encoder
from Database.CscartModels import CscartCompanies, Cscart_payments
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

from schemas.UserSchema import UserSchema

console = Console()

route = APIRouter(prefix='/admin')
templates = Jinja2Templates(directory="templates")

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
# @route.get("/user/auth", response_class=JSONResponse)
def is_authenticated(request: Request, db: Session = Depends(get_db)):
    user = LoginController.get_current_user_from_cookie(request, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    return user


@route.get("/users", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    user = LoginController.get_current_user_from_cookie(request, db)
    users = db.query(User).filter()
    context = {
        "user": user,
        "users": users,
        "request": request
    }
    return templates.TemplateResponse("users.html", context)

@route.get("/user")
def get_user(request: Request, db: Session = Depends(get_db)):
    user = LoginController.get_current_user_from_cookie(request, db)
    if user:
        user = UserSchema(**jsonable_encoder(user))
    return {"user":user}


@route.get("/users/{type}/list", response_model=List[UserSchema], responses={200:{"model": UserSchema}})#, response_model=list(UserSchema)
def index(type: str, request: Request, db: Session = Depends(get_db)):
    # first check if the user is authenticated
    user = is_authenticated(request, db)
    # then check if the user has the right permissions(admin only)
    if not roles_checker.admin_access(user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden"
        )
    

    users = []
    if type == "vendors":
        users = db.query(User).filter(or_(User.roles == "Role_affiliate", User.roles == "Role_direct_sale")).all()
    elif type == "admins":
        users = db.query(User).filter(User.roles == "Role_admin").all()

    res = []
    for u in users:
        res.append(UserSchema(**jsonable_encoder(u)))
    return res

@route.get('/get-all-users', response_class=JSONResponse)
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    # user = LoginController.get_current_user_from_cookie(request, db)
    # console.log(user)
    users = db.query(User).all()

    datas = []

    return {'users': users}

@route.delete('/users', response_class=JSONResponse)
async def delete_user(request: Request, db: Session = Depends(get_db)):
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

@route.post('/users/', response_class=JSONResponse)
async def add_user(request: Request, db: Session = Depends(get_db)):
    try:
        datas = await request.json()
        current_user = LoginController.get_current_user_from_cookie(request, db)

        user = UserDtoCreate(**datas)

        ans = LoginController.create_user_account(user, db)

        newUser = UserDto(**datas)

        if ans:
            return {
                'status': True,
                'user': newUser
            }

        return {
                'status': False,
                'message': 'An error occured, cannot create'
            }
    except:
        return {
                'status': False,
                'message': 'An error occured',
            }
        

@route.post('/users/admins', response_class=JSONResponse)
async def add_admin_user(request: Request, db: Session = Depends(get_db)):
    try:
        datas = await request.json()
        console.log(datas)
        # current_user = is_authenticated()

        user = AdminDtoCreate(**datas)

        user.password = crypto.hash("secret")

        ans = LoginController.create_user_account(user, db)

        newUser = UserDto(**datas)

        if ans:
            return {
                'status': True,
                'user': newUser
            }

        return {
                'status': False,
                'message': 'An error occured, cannot create'
            }
    except Exception as e:
        return {
                'status': False,
                'message': 'An error occured',
                'complete error': str(e)
            }
   
    
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

