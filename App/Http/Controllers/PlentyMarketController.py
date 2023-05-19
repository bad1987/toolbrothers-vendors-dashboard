from sqlalchemy.orm import Session
from fastapi import Request, status
from fastapi.responses import JSONResponse
from App.Http.Schema.Settings.PlentyMarketSchema import PlentyMarketSchema
from rich.console import Console
from App.core.auth import LoginController

from App.output_ports.models.Models import Platform_settings
from App.output_ports.repositories.platform_repository import PlatformRepository
console = Console()

class PlentyMarketController:

    def __init__(self, db_local) -> None:
        self.db_local = db_local
        self.plat_rep = PlatformRepository(self.db_local)

    def get_plenty_market_information_by_vendor (self, request: Request):
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        if user is None:
            return None
        return self.plat_rep.get_platform_info(user.id)
        
    
    def update_or_add_setting_information(self, request: Request, schema: PlentyMarketSchema):
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        if user is None:
            return None
        
        setting = self.plat_rep.get_platform_info(user.id)
 
        if not setting:
            result = self.persist_setting_information(user.id, schema, None)
            self.plat_rep.add_setting_information(result)

            return JSONResponse(status_code=status.HTTP_201_CREATED, content='Create successful') 

        result = self.persist_setting_information(user.id, schema, setting)
        self.plat_rep.update_setting_information(result)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Update successful') 
    
    # Persist information 
    def persist_setting_information(self, user_id, schema: PlentyMarketSchema, setting):
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