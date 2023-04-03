import time
from fastapi import Depends, HTTPException,Request, APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.ProductController import ProductController
from Database.Models import Payment_method
from typing import List
from Security.Acls.RoleChecker import Role_checker
from fastapi.encoders import jsonable_encoder
from Routes.Users import is_authenticated
from App.Http.Schema.ProductSchema import ProductSchema

console = Console()


roles_checker = Role_checker()

route = APIRouter(prefix='/products')
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


def timestamp_to_date(s):
    return time.ctime(s)

@route.get('/list')
async def getProductListByVendor(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), skip: int = 0, limit: int = 10):
    user = is_authenticated(request, db_local)
    if not roles_checker.vendors_access(user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden"
        )
    result = ProductController.get_product_list_by_vendor(request, db_local, db_cscart, skip, limit)
    
    data = []
    for p in result['products']:
        temp = ProductSchema(**jsonable_encoder(p))
        console.log(jsonable_encoder(temp.cscart_product_prices))
        data.append(temp)
    return {"products": data, "total": result["total"]}