from fastapi import APIRouter, Depends, Request
from App.core.auth.auth import validate_token
from App.core.use_cases.order_use_case import OrderUsecase

from App.input_ports.schemas.OrderSchema import OrderResponseModel
from App.output_ports.db.Connexion import SessionLocal
from App.output_ports.db.CscartConnexion import CscartSession
from sqlalchemy.orm import Session

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

api_route = APIRouter(prefix='/api', tags=['Orders system'], include_in_schema=True)

@api_route.get('/orders/list/', response_model=OrderResponseModel)
async def get_all_orders(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), payload: dict = Depends(validate_token), skip: int = 0, limit: int = 10):
    order_usecase = OrderUsecase()
    result = order_usecase.get_order_list(request=request, db_cscart=db_cscart, db_local=db_local,skip=skip, limit=limit)
    return result