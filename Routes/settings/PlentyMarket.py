import time
from fastapi import Depends,Request, APIRouter
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.PlentyMarketController import PlentyMarketController
from typing import List
from schemas.Settings.PlentyMarketSchema import PlentyMarketSchema
from fastapi.encoders import jsonable_encoder
from Routes.Users import is_authenticated

console = Console()

route = APIRouter(prefix='/plenty-market')


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


def timestamp_to_date(s):
    return time.ctime(s)

@route.get('/vendor', response_model=List[PlentyMarketSchema], responses={200:{"model": PlentyMarketSchema}})
def get_plenty_market_information(request: Request, db_local: Session = Depends(get_db)):
    is_authenticated(request, db_local)
    result = PlentyMarketController.get_plenty_market_information_by_vendor(request, db_local)
    res = []
    for u in result:
        res.append(PlentyMarketSchema(**jsonable_encoder(u)))
    return res

@route.post('/update')
def update_or_create(request: Request, schema: PlentyMarketSchema, db_local: Session = Depends(get_db)):
    return PlentyMarketController.update_or_add_setting_information(request, schema, db_local)