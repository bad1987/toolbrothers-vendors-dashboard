from datetime import datetime, time
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, select, join
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, Response, status
from App.Enums.OrderEnums import OrderOrderBy, SortOrder
from App.core.auth import LoginController
from App.core.entities.product_repository import IProductRepository
from App.input_ports.schemas.ProductSchema import ProductListResponseSchema, ProductSchema
from App.output_ports.models.CscartModels import Cscart_product_descriptions, Cscart_product_prices, Cscart_products
from App.output_ports.models.Models import User




class ProductRepository(IProductRepository):

    def __init__(self, db_local: Session, db_cscart: Session) -> None:
        super().__init__()
        self.db_local = db_local
        self.db_cscart = db_cscart

    def get_products(self,request: Request, statuses: list, skip: int, limit: int) -> ProductListResponseSchema:
        user = LoginController.get_current_user_from_cookie(request, self.db_local)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        company_id = user.company_id
                    
        query = self.db_cscart.query(Cscart_products).filter(Cscart_products.company_id == company_id)

        if user.parent_id != None:
            parent = self.db_local.query(User).filter(User.id == user.parent_id).first()
            company_id = parent.company_id
            query = self.db_cscart.query(Cscart_products).filter(Cscart_products.company_id == company_id)

        total = query.count()

        query = select(Cscart_products,Cscart_product_descriptions, Cscart_product_prices, Cscart_product_descriptions).where(Cscart_products.company_id == company_id).\
                    select_from(join(Cscart_products, Cscart_product_descriptions, Cscart_product_descriptions.product_id == Cscart_products.product_id)).\
                    join(Cscart_product_prices, Cscart_product_prices.product_id == Cscart_products.product_id).\
                    where(Cscart_product_descriptions.lang_code == user.default_language.value).\
                    filter(Cscart_products.status.in_(statuses)).\
                    order_by(Cscart_products.timestamp.desc()).\
                    offset(skip).limit(limit)

        products = self.db_cscart.execute(query).all()

        data = [{ **p[0].__dict__, **p[1].__dict__, **p[2].__dict__} for p in products]


        return {"products": data, "total": total}

    def get_product(self,product_id: int, request: Request) -> ProductSchema:

        user = LoginController.get_current_user_from_cookie(request, self.db_local)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        query = select(Cscart_products,Cscart_product_descriptions, Cscart_product_prices, Cscart_product_descriptions).where(Cscart_products.company_id == user.company_id).\
                where(Cscart_products.product_id == product_id).\
                where(Cscart_product_descriptions.lang_code == user.default_language.value).\
                select_from(join(Cscart_products, Cscart_product_descriptions, Cscart_product_descriptions.product_id == Cscart_products.product_id)).\
                join(Cscart_product_prices, Cscart_product_prices.product_id == Cscart_products.product_id)

        result = self.db_cscart.execute(query).first()

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
    
    def get_product_stats(self, company_id):
        # count the number of active products and out of stock products based on connected vendor
        active_products = self.db_cscart.query(func.sum(func.if_(Cscart_products.status == 'A', 1, None))).filter(Cscart_products.company_id == company_id).scalar()
        out_of_stock_products = self.db_cscart.query(func.sum(func.if_(Cscart_products.amount == 0, 1, None))).filter(Cscart_products.company_id == company_id).scalar()

        # replace None with 0 for active_products and out_of_stock_products
        active_products = active_products or 0
        out_of_stock_products = out_of_stock_products or 0

        return {
            'active_products': active_products,
            'out_of_stock': out_of_stock_products
        }