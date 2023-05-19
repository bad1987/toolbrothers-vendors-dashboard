
from abc import ABC, abstractmethod

from fastapi import Request



class ISettingRepository(ABC):
    
    def generate_token_for_api(self, request: Request):
        ...
    
    def get_token_api(self, request: Request):
        ...