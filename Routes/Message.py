import time
from fastapi import Depends,Request, APIRouter
from fastapi.responses import JSONResponse
from App.Http.Schema.MessageSchema import CscartUserSchema, MessageSchema, ChatSchema
from Security.Acls.RoleChecker import Role_checker
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.MessageController import MessageController
from fastapi.encoders import jsonable_encoder


console = Console()

route = APIRouter(prefix='', tags=['Message center'])


roles_checker = Role_checker()

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

@route.get("/messages", response_class=JSONResponse)
async def get_last_message(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), skip: int = 0, limit: int = 10):

    result = MessageController.get_last_message(request, db_local, db_cscart, skip, limit)
    
    data = []
    for p in result['messages']:
        temp = MessageSchema(**jsonable_encoder(p[0]))
        temp.setUser(CscartUserSchema(**jsonable_encoder(p[1])))
        data.append(temp)
        
    return {"messages": data, "total": result["total"]}

@route.get('/message/chat/{thread_id}/{user_id}', response_class=JSONResponse)
async def get_all_message_by_thread(request: Request, thread_id: int, user_id: int, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart)):
    result = MessageController.get_all_message_with_thread(request, thread_id, user_id, db_local, db_cscart)
    
    data = []
    for p in result:
        temp = ChatSchema(**jsonable_encoder(p[0]))
        temp.setUser(CscartUserSchema(**jsonable_encoder(p[1])))
        data.append(temp)
        
    return data


@route.post('/chat/send')
async def send_message(request: Request, chatSchema: ChatSchema, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart)):
    return MessageController.send_message(request, chatSchema, db_local, db_cscart)
