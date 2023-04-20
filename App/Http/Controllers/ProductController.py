from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, join
from sqlalchemy.sql import text
from fastapi import Request, status, HTTPException
from Security.Controllers import LoginController
from Database.CscartModels import Cscart_product_descriptions, Cscart_products, Cscart_product_prices
from fastapi.responses import JSONResponse
from schemas.Settings.PlentyMarketSchema import PlentyMarketSchema
from rich.console import Console
from schemas.UserSchema import UserSchema
from App.Http.Schema.ProductSchema import ProductSchema
from fastapi.encoders import jsonable_encoder
console = Console()

class ProductController:
    def get_product_list_by_vendor(request: Request, db_local: Session, db_cscart: Session, skip: int, limit: int):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        if not user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied') 
                    
        query = db_cscart.query(Cscart_products).filter(Cscart_products.company_id == user.company_id)
        total = query.count()

        query = select(Cscart_products,Cscart_product_descriptions, Cscart_product_prices, Cscart_product_descriptions).where(Cscart_products.company_id == user.company_id).\
                    select_from(join(Cscart_products, Cscart_product_descriptions, Cscart_product_descriptions.product_id == Cscart_products.product_id)).\
                    join(Cscart_product_prices, Cscart_product_prices.product_id == Cscart_products.product_id).\
                    where(Cscart_product_descriptions.lang_code == user.default_language.value).\
                    order_by(Cscart_products.timestamp.desc()).\
                    offset(skip).limit(limit)

        products = db_cscart.execute(query).all()

        return {"products": products, "total": total}

    def get_product_by_id(product_id: int, request: Request, db_cscart: Session, user: UserSchema):
        query = select(Cscart_products,Cscart_product_descriptions, Cscart_product_prices, Cscart_product_descriptions).where(Cscart_products.company_id == user.company_id).\
                where(Cscart_products.product_id == product_id).\
                select_from(join(Cscart_products, Cscart_product_descriptions, Cscart_product_descriptions.product_id == Cscart_products.product_id)).\
                join(Cscart_product_prices, Cscart_product_prices.product_id == Cscart_products.product_id)

        product = db_cscart.execute(query).first()

        return product
