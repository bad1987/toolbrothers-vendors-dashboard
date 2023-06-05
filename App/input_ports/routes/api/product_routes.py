from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Request
from App.Enums.OrderEnums import OrderOrderBy, OrderStatus, SortOrder
from App.Enums.ProductEnums import ProductStatus
from App.core.auth.auth import validate_token
from App.core.use_cases.order_use_case import OrderUsecase
from App.core.use_cases.product_use_case import ProductUseCase

from App.input_ports.schemas.OrderSchema import OrderResponseModel, SingleOrderResponseModel
from App.input_ports.schemas.ProductSchema import ProductListResponseSchema, ProductSchema
from App.output_ports.db.Connexion import SessionLocal
from App.output_ports.db.CscartConnexion import CscartSession
from sqlalchemy.orm import Session

from App.core.auth.auth import validate_token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_cscart():
    db_cscart = CscartSession()
    try:
        yield db_cscart
    finally:
        db_cscart.close()

api_route = APIRouter(prefix='/api', tags=['Products system'], include_in_schema=False)

@api_route.get('/products', response_model=ProductListResponseSchema)
def get_product_list(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart),
        payload: dict = Depends(validate_token), page: int = Query(1, ge=1), items_per_page: int = 10,
        statuses: List[ProductStatus] = Query([ProductStatus.ACTIVE.value, ProductStatus.DISABLED.value, ProductStatus.HIDDEN.value],
        description="The status of the product. Available options are: A - Active, H - Hidden, D - Disable"),
    ):
    product_usecase = ProductUseCase(db_local=db_local, db_cscart=db_cscart)

    result = product_usecase.get_product_list(request, [status.value for status in statuses], skip = (page - 1) * items_per_page, limit=items_per_page)

    return result

@api_route.get("/products/{product_id}", response_model=ProductSchema | None)
def get_product(
      product_id: int,
      request: Request,
      db_local: Session = Depends(get_db),
      db_cscart: Session = Depends(get_db_cscart),
      payload: dict = Depends(validate_token),
    ):
    product_usecase = ProductUseCase(db_local=db_local, db_cscart=db_cscart)

    return product_usecase.get_product(request, product_id)