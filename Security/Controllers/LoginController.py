
import datetime as dt
from typing import Dict, List, Optional
from Security.OAuth2PasswordBearerWithCookie import OAuth2PasswordBearerWithCookie
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from rich import print
from Security.Settings import Settings
from Security.DTO.UserDto import UserDto
from Security.DTO.UserDto import UserDtoCreate
from Security.DTO.DataBase import DataBase
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from Database.Models import User
from rich.console import Console
from Database.Connexion import SessionLocal
import json

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

console = Console()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        Settings.SECRET_KEY, 
        algorithm=Settings.ALGORITHM
    )
    return encoded_jwt


def authenticate_user(username: str, plain_password: str, db: Session) -> UserDto:
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not crypto.verify(plain_password, user.password):
        return False
    return user


def decode_token(token: str, db: Session) -> UserDto:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials."
    )
    token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    user = get_user_by_email(db, username)
    return user


def get_current_user_from_token(db: Session, token: str = Depends(oauth2_scheme)) -> UserDto:
    """
    Get the current user from the cookies in a request.

    Use this function when you want to lock down a route so that only 
    authenticated users can see access the route.
    """
    console.log(f"[green]{token}")
    user = decode_token(token, db)
    return user


def get_current_user_from_cookie(request: Request, db: Session) -> UserDto:
    """
    Get the current user from the cookies in a request.
    
    Use this function from inside other routes to get the current user. Good
    for views that should work for both logged in, and not logged in users.
    """
    token = request.cookies.get(Settings.COOKIE_NAME)
    user = decode_token(token, db)
    return user

# Register user
def create_user_account(user_dto: UserDtoCreate, db: Session):
    user = User()
    is_user = db.query(User).filter(User.email == user_dto.email).first()
    if not is_user:
        user.username = user_dto.username
        user.email = user_dto.email
        user.password = crypto.hash(user_dto.password)
        user.roles = "ad"
        user.status = "A"
        user.company_id = 10
        
        db.add(user)
        db.commit()

        db.flush(user)

        
        return user
    return False

def is_authenticated(request: Request):
    db = SessionLocal()
    try:
        user = get_current_user_from_cookie(request, db)
    except Exception as e:
        print(str(e))
        user = None
    finally:
        db.close()
    return user