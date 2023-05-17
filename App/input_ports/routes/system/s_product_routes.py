import time, traceback, sys
from fastapi import Depends, HTTPException,Request, APIRouter, status, Response
from fastapi.responses import HTMLResponse, JSONResponse
from App.Enums.UserRoleEnum import ModelNameEnum
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.ProductController import ProductController
from typing import List, Dict
from fastapi.encoders import jsonable_encoder
from App.Http.Schema.ProductSchema import ProductSchema, ProductListSchemaOut, ProductUpdateSchemaIn
from App.Http.Schema.ProductPriceSchema import ProductPriceSchema
from App.core.Decorators.auth_decorators import requires_permission
from App.core.auth.Acls.RoleChecker import Role_checker
from App.core.auth.auth import is_authenticated
from App.core.dependencies.db_dependencies import get_db, get_db_cscart
from App.output_ports.models.Models import User


roles_checker = Role_checker()

route = APIRouter(prefix='/products', tags=['Import products from cs-cart'], include_in_schema=False)

@route.get('/list')
@requires_permission('read', ModelNameEnum.PRODUCT_MODEL.value)
async def getProductListByVendor(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated), skip: int = 0, limit: int = 10):
    result = ProductController.get_product_list_by_vendor(_user,request, db_local, db_cscart, skip, limit)
    
    data = [{ **p[0].__dict__, **p[1].__dict__, **p[2].__dict__} for p in result['products']]

    return {"products": data, "total": result["total"]}

@route.put('/{product_id}', response_model = ProductSchema | Dict[str, str])
@requires_permission('write', ModelNameEnum.PRODUCT_MODEL.value)
async def update_product(request: Request,model: ProductUpdateSchemaIn, product_id: int, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated)):
    return ProductController.update_product(product_id, model, request, db_local, db_cscart)


@route.get("/stats")
async def get_product_stats(request: Request, db_cscart: Session = Depends(get_db_cscart)):
    ProductController.get_product_stats(db_cscart, 4)