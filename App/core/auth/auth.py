from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from App.core.auth.Configs.Settings import Settings

security = HTTPBearer()

async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # validate token
    try:
        payload = jwt.decode(str(credentials.credentials.removeprefix("Bearer").strip()), Settings.SECRET_KEY, algorithms=Settings.ALGORITHM)
        return True if payload else False
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")