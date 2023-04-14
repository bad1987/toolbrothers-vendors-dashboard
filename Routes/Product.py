import time
from fastapi import Depends, HTTPException,Request, APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from App.Enums.UserRoleEnum import ModelNameEnum
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.ProductController import ProductController
from Database.Models import Payment_method
from typing import List
from Decorators.auth_decorators import requires_permission, requires_vendor_access
from Security.Acls.RoleChecker import Role_checker
from fastapi.encoders import jsonable_encoder
from Routes.Users import is_authenticated
from App.Http.Schema.ProductSchema import ProductSchema
from App.Http.Schema.ProductPriceSchema import ProductPriceSchema

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
@requires_permission('read', ModelNameEnum.USER_MODEL.value)
async def getProductListByVendor(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated), skip: int = 0, limit: int = 10):
    result = ProductController.get_product_list_by_vendor(request, db_local, db_cscart, skip, limit)
    
    data = []
    for p in result['products']:
        temp = ProductSchema(**jsonable_encoder(p[0]))
        temp.setPrices(ProductPriceSchema(**jsonable_encoder(p[1])))
        temp.setProductName(p[2])
        data.append(temp)
    return {"products": data, "total": result["total"]}