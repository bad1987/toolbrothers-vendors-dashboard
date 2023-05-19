from datetime import datetime, time, timedelta
from typing import List, Optional
import jwt
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func, text
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, Request, status
from App.Enums.OrderEnums import OrderOrderBy, SortOrder
from App.core.Services.Security.Settings import Settings
from App.core.auth import LoginController
from fastapi.responses import JSONResponse

import phpserialize
from App.core.entities.settings.ISettingRepository import ISettingRepository
from App.output_ports.models.Models import User


class SettingRepository(ISettingRepository):
    def __init__(self, db_local: Session):
        self.db_local = db_local
        
    def generate_token_for_api (self, request: Request):
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        userToken = self.db_local.query(User).filter(User.id == user.id).first()
        
        expire_time = datetime.utcnow() + timedelta(days=Settings.API_TOKEN_EXPIRE_DAYS)
        playload = {"exp": expire_time, "email": userToken.email}
        encoded_token = jwt.encode(playload, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
        
        userToken.api_token = encoded_token
        self.db_local.commit()
        
        return encoded_token
 
    def get_token_api (self, request: Request):
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        userToken = self.db_local.query(User).filter(User.id == user.id).first()
        
        return userToken.api_token