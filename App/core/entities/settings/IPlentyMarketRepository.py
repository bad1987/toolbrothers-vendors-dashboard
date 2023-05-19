
from abc import ABC, abstractmethod
from typing import List, Optional

from fastapi import Request
from sqlalchemy.orm import Session

from App.input_ports.schemas.Settings.PlentyMarketSchema import PlentyMarketSchema


class IPlentyMarketRepository(ABC):
    
    def get_plenty_market_information_by_vendor(self, request: Request)->List[PlentyMarketSchema]:
        ...
    
    def update_or_add_setting_information(self, request: Request, schema: PlentyMarketSchema):
        ...