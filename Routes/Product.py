import time
from fastapi import Depends, HTTPException,Request, APIRouter, status, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from App.Enums.UserRoleEnum import ModelNameEnum
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.ProductController import ProductController
from Database.Models import Payment_method
from typing import List, Dict
from Decorators.auth_decorators import requires_permission, requires_vendor_access
from Security.Acls.RoleChecker import Role_checker
from fastapi.encoders import jsonable_encoder
from Routes.Users import is_authenticated
from App.Http.Schema.ProductSchema import ProductSchema, ProductUpdateSchema
from App.Http.Schema.ProductPriceSchema import ProductPriceSchema
from Security.Controllers import LoginController
from Database.CscartModels import Cscart_product_descriptions, Cscart_products, Cscart_product_prices

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
@requires_permission('read', ModelNameEnum.PRODUCT_MODEL.value)
async def getProductListByVendor(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated), skip: int = 0, limit: int = 10):
    result = ProductController.get_product_list_by_vendor(request, db_local, db_cscart, skip, limit)
    
    data = []
    for p in result['products']:
        temp = ProductSchema(**jsonable_encoder(p[0]))
        temp.setPrices(ProductPriceSchema(**jsonable_encoder(p[1])))
        temp.setProductName(p[2])
        data.append(temp)
    return {"products": data, "total": result["total"]}

@route.put('/{product_id}', response_model = ProductUpdateSchema | Dict[str, str])
@requires_permission('write', ModelNameEnum.PRODUCT_MODEL.value)
async def update_product(request: Request,model: ProductUpdateSchema, product_id: int,response: Response, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated)):
    try:
        user = LoginController.get_current_user_from_cookie(request, db_local)

        # product = db_cscart.query(Cscart_products).filter(Cscart_products.product_id == product_id).first()
        # price = db_cscart.query(Cscart_product_prices).filter(Cscart_product_prices.product_id == product_id).first()

        # if product is None:
        #     response.status_code = status.HTTP_404_NOT_FOUND
        #     return { 'status': False, 'message': 'Product not found' }

        # if user.company_id != product.company_id:
        #     response.status_code = status.HTTP_401_UNAUTHORIZED
        #     return { 'status': False, 'message': 'You are not authorize to access this product' }

        # # Modify the product
        # for field, value in model.dict(exclude_unset=True).items():
        #     setattr(product, field, value)

        # #modify price
        # for field, value in model.dict(exclude_unset=True).items():
        #     setattr(price, field, value)

        product_model = ProductController.get_product_by_id(product_id, request, db_cscart, user)

        return product_model
    
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return { 'status': False, 'message': 'An error occured' }