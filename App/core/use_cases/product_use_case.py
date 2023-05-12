from datetime import datetime
from typing import List

from fastapi import Depends, Request
from App.input_ports.schemas.OrderSchema import OrderResponseModel, SingleOrderResponseModel
from App.input_ports.schemas.ProductSchema import ProductListResponseSchema, ProductSchema

from App.output_ports.repositories.order_repository import OrderRepository

from sqlalchemy.orm import Session

from App.output_ports.repositories.product_repository import ProductRepository

class ProductUseCase():
    def __init__(self, product_repo: ProductRepository = ProductRepository()) -> None:
        self.product_repository = product_repo

    def get_product_list(self, request: Request, db_local: Session, db_cscart: Session,
        statuses: list, skip: int, limit: int) -> ProductListResponseSchema:
        return self.product_repository.get_products(request, db_local, db_cscart, statuses, skip, limit)

    def get_product(self, request: Request, product_id: int, db_local: Session, db_cscart: Session) -> ProductSchema:
        return self.product_repository.get_product(product_id, request, db_local, db_cscart)