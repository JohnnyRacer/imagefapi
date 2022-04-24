from __future__ import annotations

from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, Optional, Union

import jwt
from jwt import PyJWTError
from fastapi import APIRouter, Body, Depends, Form, HTTPException,Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext
from pydantic import BaseModel

from app.core import config

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
router = APIRouter()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


fake_users_db = {
    "ubuntu": {
        "username": config.API_USERNAME,
        "hashed_password": get_password_hash(config.API_PASSWORD),
    }
}


def get_user(
    db: dict[str, dict[str, str]],
    username: Optional[str],
) -> UserInDB:

    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(
    fake_db: dict[str, dict[str, str]],
    username: str,
    password: str,
) -> Union[bool, UserInDB]:

    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def read_pemk(key_fp:str,ret_bytes:bool=True):
    with open(key_fp, 'r') as kfb:
        key = kfb.read()
    if ret_bytes:
        return key.encode()
    return key

jwt_prv_key = read_pemk('test_keys/jwt-key')

jwt_pub_key = read_pemk('test_keys/jwt-key.pub' ,ret_bytes=False)

def create_access_token(data: dict, expires_delta: timedelta = None, access_ip: str = None) -> bytes:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=15)

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        
    to_encode.update({"exp": expire})
    to_encode.update({"ip":access_ip})
    encoded_jwt = jwt.encode(
        to_encode,
        jwt_prv_key,
        algorithm=config.API_ALGORITHM,
    )
    return encoded_jwt


class VerifyToken(BaseModel):
    token:str
    token_type:str    




@router.post("/verify_token")
async def verf_token(
    token_obj: VerifyToken = Body(...)
):


    user, ip = await get_current_user(token_obj.token)

    """

        credentials_exception = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token_obj.token,
                jwt_pub_key,
                algorithms=[config.API_ALGORITHM],
            )
            print(payload)
            username = payload.get("sub")
            ip = payload.get("ip")
            print(f"Acces IP is : {ip} ")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)

        except PyJWTError:
            raise credentials_exception

        

        if user is None:
            raise credentials_exception
    """
    #print(f"Access IP : {access_ip} ")
    return {"username":user.username , "token_type":token_obj.token_type, "access_ip":ip}



async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            jwt_pub_key,
            algorithms=[config.API_ALGORITHM],
        )
        username = payload.get("sub")
        ip = payload.get('auth_ip')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except PyJWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)

    if user is None:
        raise credentials_exception
    return user, ip


@router.post("/token", response_model=Token)
async def login_for_access_token(
    request:Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    token_expiry:int=0
) -> dict[str, Any]:
    user = authenticate_user(
        fake_users_db,
        form_data.username,
        form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        seconds=config.API_ACCESS_TOKEN_EXPIRE_MINUTES if token_expiry is 0 else token_expiry,
    )
    
    not bool(int(config.DEBUG)) or print(type(form_data.scopes)) 
    print(type(form_data.client_id))
    ip = request.client.host
    print(f"Client ip is {ip} ")
    access_token = create_access_token(
        data={"sub": user.username, 'auth_ip':request.client.host},  # type: ignore
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token,"token_type": "bearer", "authed_scopes":form_data.scopes}
