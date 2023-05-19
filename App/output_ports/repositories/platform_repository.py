

from App.output_ports.models.Models import Platform_settings
from sqlalchemy.orm import Session

class PlatformRepository:

    def __init__(self, db_local: Session) -> None:
        self.db_local = db_local


    def get_platform_info(self, user_id: int):
        setting = self.db_local.query(Platform_settings).filter(Platform_settings.user_id == user_id).all()
        
        return setting
    
    def add_setting_information(self, setting: Platform_settings):
        self.db_local.add(setting)
        self.db_local.commit()
        self.db_local.flush(setting)

        return setting
    

    def update_setting_information(self, setting: Platform_settings):
        self.db_local.commit()
        self.db_local.flush(setting)

        return setting