from typing import List
from fastapi import HTTPException, Request, status
from App.core.Services.SendEmail import send_email
from App.core.auth.Acls.ModelPermissions import ModelPermissions
from App.core.auth.LoginController import get_current_user_from_cookie
from App.input_ports.schemas.Settings.PlentyMarketSchema import PlentyMarketSchema

from sqlalchemy.orm import Session

from App.output_ports.repositories.settings.PlentyMarketRepository import PlentyMarketRepository


class PlentyMarketUseCase:
    
    def __init__(self, db_local: Session):
        self.plenty_market = PlentyMarketRepository(db_local)
        self.db_local = db_local
        
    def get_plenty_market_information_by_vendor(self, request: Request)->PlentyMarketSchema:
        _user = get_current_user_from_cookie(request=request, db=self.db_local)
        model_permissions = ModelPermissions(_user)
        
        return self.plenty_market.get_plenty_market_information_by_vendor(request)
    
    def update_or_add_setting_information(self, request: Request, schema: PlentyMarketSchema):
        _user = get_current_user_from_cookie(request, self.db_local)
        model_permissions = ModelPermissions(_user)
        
        return self.plenty_market.update_or_add_setting_information(request, schema)
        