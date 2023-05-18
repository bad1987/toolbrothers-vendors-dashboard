

from abc import ABC, abstractmethod

from App.output_ports.models.Models import Login_Attempt


class IAuthenticationRepository(ABC):

    @abstractmethod
    def get_attempts(self, connected_ip: str) -> Login_Attempt:
        ...
    
    @abstractmethod
    def create_attempt(self,connected_ip: str) -> Login_Attempt:
        ...
    
    @abstractmethod
    def increment_attempt(self,connected_ip: str) -> Login_Attempt:
        ...
    
    @abstractmethod
    def reset_attempt(self, connected_ip: str) -> Login_Attempt:
        ...