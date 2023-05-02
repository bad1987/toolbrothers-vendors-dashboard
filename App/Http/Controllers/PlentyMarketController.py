from sqlalchemy.orm import Session
from fastapi import Request, status, HTTPException
from Security.Controllers import LoginController
from Database.Models import Platform_settings
from fastapi.responses import JSONResponse
from App.Http.Schema.Settings.PlentyMarketSchema import PlentyMarketSchema
from rich.console import Console
console = Console()

class PlentyMarketController:
    def get_plenty_market_information_by_vendor (request: Request, db_local: Session):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        setting = db_local.query(Platform_settings).filter(Platform_settings.user_id == user.id).all()
        
        return setting
    
    def update_or_add_setting_information(request: Request, schema: PlentyMarketSchema, db_local: Session):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        setting = db_local.query(Platform_settings).filter(Platform_settings.user_id == user.id).first()
 
        if not setting:
            result = PlentyMarketController.persist_setting_information(request, user.id, schema, None)
            db_local.add(result)
            db_local.commit()
            db_local.flush(result)

            return JSONResponse(status_code=status.HTTP_201_CREATED, content='Create successful') 

        result = PlentyMarketController.persist_setting_information(request, user.id, schema, setting)
        db_local.commit()
        db_local.flush(result)

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