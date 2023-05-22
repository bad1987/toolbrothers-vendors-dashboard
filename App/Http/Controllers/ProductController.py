from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func, literal_column, select, join
from sqlalchemy.sql import text
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from App.Http.Schema.Settings.PlentyMarketSchema import PlentyMarketSchema
from rich.console import Console
from fastapi.encoders import jsonable_encoder
from App.core.auth import LoginController
from App.input_ports.schemas import ProductSchema, UserSchema
from App.output_ports.models.CscartModels import Cscart_product_descriptions, Cscart_product_prices, Cscart_products

from App.output_ports.models.Models import User

console = Console()

class ProductController:
    def get_product_list_by_vendor(user: User, request: Request, db_local: Session, db_cscart: Session, skip: int, limit: int, statuses: list):
        if not user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied') 

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

    def update_product(product_id: int, model: ProductSchema, request: Request, db_local: Session, db_cscart: Session):
        try:
            if db_cscart.in_transaction():
                db_cscart.rollback()
            transaction = db_cscart.begin()
            user = LoginController.get_current_user_from_cookie(request, db_local)

            product = db_cscart.query(Cscart_products).filter(Cscart_products.product_id == product_id).filter(Cscart_products.company_id == user.company_id).first()
            price = product.price

            if product is None:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product Not Found"
            )

            if user.company_id != product.company_id:
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not able to access this product"
            )

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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occured"
            )