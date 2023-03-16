from fastapi import Depends,Request, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from Security.Controllers import LoginController
from Security.DTO.UserDto import UserDtoCreate
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from Database.Models import User
from rich.console import Console
from fastapi.encoders import jsonable_encoder
from Database.CscartModels import CscartCompanies
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

console = Console()



route = APIRouter(prefix='')
templates = Jinja2Templates(directory="templates")



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

@route.get('/get-all-users', response_class=JSONResponse)
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    user = LoginController.get_current_user_from_cookie(request, db)
    console.log(user)
    users = db.query(User).all()

    return {'users': users}

@route.post('/users/', response_class=JSONResponse)
async def add_user(request: Request, db: Session = Depends(get_db)):
    try:
        datas = await request.json()
        current_user = LoginController.get_current_user_from_cookie(request, db)

        user = UserDtoCreate(**datas)

        ans = LoginController.create_user_account(user, db)


        if ans:
            return {
                'status': True,
                'message': 'OK',
                'current_user': current_user
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
            user.roles = "af" if item.company_id == 4 | 205 else "dp"
            user.status = item.status
            
            db_local.add(user)
            db_local.commit()
            db_local.flush(user)
            
            console.log("Add success", user.username)
    except Exception as e:
        console.log("error ...", str(e))
    
    