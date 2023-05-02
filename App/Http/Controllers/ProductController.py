from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func, literal_column, select, join
from sqlalchemy.sql import text
from fastapi import Request, status, HTTPException
from Security.Controllers import LoginController
from Database.CscartModels import Cscart_product_descriptions, Cscart_products, Cscart_product_prices
from fastapi.responses import JSONResponse
from App.Http.Schema.Settings.PlentyMarketSchema import PlentyMarketSchema
from rich.console import Console
from App.Http.Schema.UserSchema import UserSchema
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

    def get_product_by_id(product_id: int, request: Request, db_cscart: Session, user: UserSchema) -> ProductSchema:
        query = select(Cscart_products,Cscart_product_descriptions, Cscart_product_prices, Cscart_product_descriptions).where(Cscart_products.company_id == user.company_id).\
                where(Cscart_products.product_id == product_id).\
                where(Cscart_product_descriptions.lang_code == user.default_language.value).\
                select_from(join(Cscart_products, Cscart_product_descriptions, Cscart_product_descriptions.product_id == Cscart_products.product_id)).\
                join(Cscart_product_prices, Cscart_product_prices.product_id == Cscart_products.product_id)

        result = db_cscart.execute(query).first()

        product = ProductSchema(
            product=result.Cscart_product_descriptions.product,
            product_id=result.Cscart_products.product_id,
            manual_change=result.Cscart_products.manual_change,
            product_code=result.Cscart_products.product_code,
            amount=result.Cscart_products.amount,
            product_type=result.Cscart_products.product_type,
            status=result.Cscart_products.status,
            weight=result.Cscart_products.weight,
            price=result.Cscart_product_prices.price,
        )

        return product

    def get_product_stats(db_cscart: Session, company_id):
        # count the number of active products and out of stock products based on connected vendor
        active_products = db_cscart.query(func.sum(func.if_(Cscart_products.status == 'A', 1, None))).filter(Cscart_products.company_id == company_id).scalar()
        out_of_stock_products = db_cscart.query(func.sum(func.if_(Cscart_products.amount == 0, 1, None))).filter(Cscart_products.company_id == company_id).scalar()

        # replace None with 0 for active_products and out_of_stock_products
        active_products = active_products or 0
        out_of_stock_products = out_of_stock_products or 0

        return {
            'active_products': active_products,
            'out_of_stock': out_of_stock_products
        }
