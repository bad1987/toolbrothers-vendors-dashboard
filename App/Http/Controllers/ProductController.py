from sqlalchemy.orm import Session
from fastapi import Request, status, HTTPException
from Security.Controllers import LoginController
from Database.CscartModels import Cscart_product_descriptions, Cscart_products, Cscart_product_prices
from fastapi.responses import JSONResponse
from schemas.Settings.PlentyMarketSchema import PlentyMarketSchema
from rich.console import Console
console = Console()

class ProductController:
    def get_product_list_by_vendor(request: Request, db_local: Session, db_cscart: Session, skip: int, limit: int):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        if not user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied') 
       
        # query = db_cscart.query(Cscart_products).\
        #     filter(Cscart_products.company_id == user.company_id)
        query = db_cscart.query(Cscart_products, Cscart_product_prices).\
            join(Cscart_product_prices, Cscart_product_prices.product_id == Cscart_products.product_id).\
            filter(Cscart_products.company_id == user.company_id)
            # add_columns(Cscart_product_prices.price)
            
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        print(products)
            
        return {"products": products, "total": total}