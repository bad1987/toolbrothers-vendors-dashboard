
import random
import string
from typing import List
from fastapi import HTTPException, status, Request

from sqlalchemy import and_
from App.core.entities.settings.IPlentyMarketRepository import IPlentyMarketRepository
from App.core.entities.settings.payment_method_repository import IPaymentRepository
from sqlalchemy.orm import Session
from App.input_ports.schemas.Settings.PaymentMethodSchema import PaymentMethodSchema
from App.core.auth.LoginController import get_current_user_from_cookie
from App.core.auth import LoginController
from fastapi.responses import JSONResponse
from App.input_ports.schemas.Settings.PlentyMarketSchema import PlentyMarketSchema

from App.output_ports.models.Models import Platform_settings


class PlentyMarketRepository(IPlentyMarketRepository):
    def __init__(self, db_local: Session):
        self.db_local = db_local
        
    def get_plenty_market_information_by_vendor (self, request: Request):
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        setting = self.db_local.query(Platform_settings).filter(Platform_settings.user_id == user.id).all()
        
        return setting
    
    def update_or_add_setting_information(self, request: Request, schema: PlentyMarketSchema):
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        setting = self.db_local.query(Platform_settings).filter(Platform_settings.user_id == user.id).first()
 
        if not setting:
            result = self.persist_setting_information(request, user.id, schema, None)
            self.db_local.add(result)
            self.db_local.commit()
            self.db_local.flush(result)

            return JSONResponse(status_code=status.HTTP_201_CREATED, content='Create successful') 

        result = self.persist_setting_information(request, user.id, schema, setting)
        self.db_local.commit()
        self.db_local.flush(result)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Update successful') 
    
    # Persist information 
    def persist_setting_information(request: Request, user_id, schema: PlentyMarketSchema, setting):
        if not setting:
            add_setting = Platform_settings()
            add_setting.user_id = user_id
        if setting:
            add_setting = setting
            
        if schema.platform_id:
            add_setting.platform_id = schema.platform_id
        if schema.referrer_id:
            add_setting.referrer_id = schema.referrer_id
        if schema.api_id:
            add_setting.api_id = schema.api_id
        if schema.api_secret:
            add_setting.api_secret = schema.api_secret
        if schema.access_token:
            add_setting.access_token = schema.access_token
        if schema.platform_url:
            add_setting.platform_url = schema.platform_url
        if schema.method_payment_id:
            add_setting.method_payment_id = schema.method_payment_id
        if schema.shipping_profile_id:
            add_setting.shipping_profile_id = schema.shipping_profile_id
        if schema.export_product_link:
            add_setting.export_product_link = schema.export_product_link
        
        return add_setting