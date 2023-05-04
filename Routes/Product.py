import time, traceback, sys
from fastapi import Depends, HTTPException,Request, APIRouter, status, Response
from fastapi.responses import HTMLResponse, JSONResponse
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
from App.Http.Schema.ProductSchema import ProductSchema, ProductListSchemaOut, ProductUpdateSchemaIn
from App.Http.Schema.ProductPriceSchema import ProductPriceSchema
from Security.Controllers import LoginController
from Database.CscartModels import Cscart_product_descriptions, Cscart_products, Cscart_product_prices

console = Console()


roles_checker = Role_checker()

route = APIRouter(prefix='/products', tags=['Import products from cs-cart'], include_in_schema=False)


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
    
    data = [{ **p[0].__dict__, **p[1].__dict__, **p[2].__dict__} for p in result['products']]

    return {"products": data, "total": result["total"]}

@route.put('/{product_id}', response_model = ProductSchema | Dict[str, str])
@requires_permission('write', ModelNameEnum.PRODUCT_MODEL.value)
async def update_product(request: Request,model: ProductUpdateSchemaIn, product_id: int,response: Response, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated)):
    try:
        if db_cscart.in_transaction():
            db_cscart.rollback()
        transaction = db_cscart.begin()
        user = LoginController.get_current_user_from_cookie(request, db_local)

        product = db_cscart.query(Cscart_products).filter(Cscart_products.product_id == product_id).filter(Cscart_products.company_id == user.company_id).first()
        price = product.price

        if product is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': False, 'message': 'Product not found' }

        if user.company_id != product.company_id:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return { 'status': False, 'message': 'You are not authorize to access this product' }

        #modify price
        for field, value in model.dict(exclude_unset=True, exclude_none=True, exclude={"product_id"}).items():
            if hasattr(price, field):
                setattr(price, field, value)

        # Modify the product
        for field, value in model.dict(exclude_unset=True, exclude={"product_id", "price"}, exclude_none=True).items():
            if hasattr(product, field):
                setattr(product, field, value)

        product_model = ProductController.get_product_by_id(product_id, request, db_cscart, user)

        db_cscart.commit()

        return product_model
    
    except Exception as e:
        # traceback.print_exc(file=sys.stdout)
        
        transaction.rollback()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return { 'status': False, 'message': "An error occured" }

@route.get("/stats")
async def get_product_stats(request: Request, db_cscart: Session = Depends(get_db_cscart)):
    ProductController.get_product_stats(db_cscart, 4)