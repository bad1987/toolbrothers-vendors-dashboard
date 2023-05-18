

import datetime
import time
from App.core.entities.authentication_repository import IAuthenticationRepository

from sqlalchemy.orm import Session

from App.output_ports.models.Models import Login_Attempt

class AuthenticationRepository(IAuthenticationRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
    

    def get_attempts(self, connected_ip: str) -> Login_Attempt:
        return self.db.query(Login_Attempt).filter(Login_Attempt.ip == connected_ip).first()
    
    def create_attempt(self,connected_ip: str) -> Login_Attempt:
        attempt = Login_Attempt()
        attempt.ip = connected_ip
        attempt.count = 1
        
        self.db.add(attempt)
        self.db.commit()

        return attempt
    
    def increment_attempt(self,connected_ip: str) -> Login_Attempt:
        attempt: Login_Attempt = self.db.query(Login_Attempt).filter(Login_Attempt.ip == connected_ip).first()
        attempt.count += 1
        if attempt.count >= 3:
            attempt.timestamp = self.get_timestamp()
        self.db.commit()

        return attempt
    
    def reset_attempt(self, connected_ip: str) -> Login_Attempt:
        attempt: Login_Attempt = self.db.query(Login_Attempt).filter(Login_Attempt.ip == connected_ip).first()
        attempt.count = 0
        self.db.commit()

        return attempt
    
    def get_timestamp(self) -> float:
        now = datetime.datetime.now()
        future = now + datetime.timedelta(minutes=1)

        timestamp = time.mktime(future.timetuple())

        return timestamp