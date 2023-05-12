from datetime import datetime, time
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, select, join
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, Response, status
from App.Enums.OrderEnums import OrderOrderBy, SortOrder
from App.core.auth import LoginController
from App.core.entities.product_repository import IProductRepository
from App.input_ports.schemas.ProductSchema import ProductListResponseSchema, ProductSchema
from App.output_ports.models.CscartModels import Cscart_product_descriptions, Cscart_product_prices, Cscart_products
from App.output_ports.models.Models import User




class ProductRepository(IProductRepository):
    def get_products(self,request: Request, db_local: Session, db_cscart: Session, statuses: list, skip: int, limit: int) -> ProductListResponseSchema:
        user = LoginController.get_current_user_from_cookie(request, db_local)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        company_id = user.company_id
                    
        query = db_cscart.query(Cscart_products).filter(Cscart_products.company_id == company_id)

        if user.parent_id != None:
            parent = db_local.query(User).filter(User.id == user.parent_id).first()
            company_id = parent.company_id
            query = db_cscart.query(Cscart_products).filter(Cscart_products.company_id == company_id)

        total = query.count()

        query = select(Cscart_products,Cscart_product_descriptions, Cscart_product_prices, Cscart_product_descriptions).where(Cscart_products.company_id == company_id).\
                    select_from(join(Cscart_products, Cscart_product_descriptions, Cscart_product_descriptions.product_id == Cscart_products.product_id)).\
                    join(Cscart_product_prices, Cscart_product_prices.product_id == Cscart_products.product_id).\
                    where(Cscart_product_descriptions.lang_code == user.default_language.value).\
                    filter(Cscart_products.status.in_(statuses)).\
                    order_by(Cscart_products.timestamp.desc()).\
                    offset(skip).limit(limit)

        products = db_cscart.execute(query).all()

        data = [{ **p[0].__dict__, **p[1].__dict__, **p[2].__dict__} for p in products]


        return {"products": data, "total": total}

    def get_product(self,product_id: int, request: Request, db_local: Session, db_cscart: Session) -> ProductSchema:

        user = LoginController.get_current_user_from_cookie(request, db_local)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        query = select(Cscart_products,Cscart_product_descriptions, Cscart_product_prices, Cscart_product_descriptions).where(Cscart_products.company_id == user.company_id).\
                where(Cscart_products.product_id == product_id).\
                where(Cscart_product_descriptions.lang_code == user.default_language.value).\
                select_from(join(Cscart_products, Cscart_product_descriptions, Cscart_product_descriptions.product_id == Cscart_products.product_id)).\
                join(Cscart_product_prices, Cscart_product_prices.product_id == Cscart_products.product_id)

        result = db_cscart.execute(query).first()

        product = None

        if result:
            product = ProductSchema(
            product_id=result.Cscart_products.product_id,
            product=result.Cscart_product_descriptions.product,
            manual_change=result.Cscart_products.manual_change,
            product_code=result.Cscart_products.product_code,
            amount=result.Cscart_products.amount,
            product_type=result.Cscart_products.product_type,
            status=result.Cscart_products.status,
            weight=result.Cscart_products.weight,
            price=result.Cscart_product_prices.price,
        )

        return product