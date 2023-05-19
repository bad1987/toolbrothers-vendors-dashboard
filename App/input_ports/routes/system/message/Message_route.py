import re
import time
from fastapi import Depends, HTTPException,Request, APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse
from App.Enums.UserRoleEnum import ModelNameEnum
from sqlalchemy.orm import Session
from rich.console import Console
from typing import List
from App.core.Decorators.auth_decorators import requires_permission
from App.core.auth.Acls.RoleChecker import Role_checker
from App.Http.Schema.Settings.PaymentMethodSchema import PaymentMethodSchema, updatePaymentMethod
from fastapi.encoders import jsonable_encoder
from App.core.auth.auth import is_authenticated
from App.core.use_cases.MessageUseCase import MessageUseCase
from App.core.use_cases.settings.PaymentUseCase import PaymentUseCase
from App.core.dependencies.db_dependencies import get_db, get_db_cscart
from App.core.auth.auth import validate_token
from App.input_ports.schemas.MessageSchema import ChatSchema, CscartUserSchema, MessageSchema

console = Console()


roles_checker = Role_checker()

route = APIRouter(prefix='', tags=['Get and send message'], include_in_schema=True)


def timestamp_to_date(s):
    return time.ctime(s)


@route.get("/messages", response_class=JSONResponse)
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def get_last_message(
    request: Request, 
    db_local: Session = Depends(get_db), 
    db_cscart: Session = Depends(get_db_cscart), 
    skip: int = 0, 
    limit: int = 10, 
    _user: dict = Depends(is_authenticated)
):

    message_use_case = MessageUseCase(db_local, db_cscart)
    result = message_use_case.get_all_message_by_vendor(request, skip, limit)
    data = []
    for p in result['messages']:
        temp = MessageSchema(**jsonable_encoder(p[0]))
        temp.setUser(CscartUserSchema(**jsonable_encoder(p[1])))
        data.append(temp)
        
    return {"messages": data, "total": result["total"]}

@route.get('/message/chat/{thread_id}/{user_id}', response_class=JSONResponse)
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def get_all_message_by_thread(
    request: Request, thread_id: int, 
    db_local: Session = Depends(get_db), 
    db_cscart: Session = Depends(get_db_cscart),
    _user: dict = Depends(is_authenticated)
    ):
    message_use_case = MessageUseCase(db_local, db_cscart)
    result = message_use_case.get_all_message_with_thread(request, thread_id, db_cscart)
    
    data = []
    for p in result:
        temp = ChatSchema(**jsonable_encoder(p[0]))
        temp.setUser(CscartUserSchema(**jsonable_encoder(p[1])))
        data.append(temp)
        
    return data


@route.post('/chat/send', response_class=JSONResponse)
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def send_message(
    request: Request, 
    chatSchema: ChatSchema, 
    db_local: Session = Depends(get_db), 
    db_cscart: Session = Depends(get_db_cscart), 
    _user: dict = Depends(is_authenticated)
    ):
    message_use_case = MessageUseCase(db_local, db_cscart)
    return message_use_case.send_message(request, chatSchema)

