from __future__ import annotations
from http import HTTPStatus
from time import time

from fastapi import APIRouter, Depends, File, HTTPException,Form, UploadFile,Request
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.rdb import *

router = APIRouter()

def get_userdb_handler(user_id:str)-> Union[dict,None]:
    if not database.check_usrid(user_id) :
        raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY ,
                detail=f"Invalid user ID string detected")
        
    return database.userdb[user_id] if database.check_usrid(user_id) else {}

@router.get("/user_stats",tags=["users_db"])
async def get_user_stats(
    auth: Depends if bool(int(config.API_AUTH_CFG)) else None = Depends(get_current_user) if bool(int(config.API_AUTH_CFG)) else None
):
    return {"users":list(database.userdb), "latest_update": database.last_update if len(list(database.userdb)) > 0 else None , "latest_user":list(database.userdb)[-1] if len(list(database.userdb)) > 0 else None }

@router.get("/random_id", tags=["users_db"])
async def get_user_stats(
    request:Request,
    auth: Depends if bool(int(config.API_AUTH_CFG)) else None = Depends(get_current_user) if bool(int(config.API_AUTH_CFG)) else None
):
    return {"random_id":database.gen_userid(), "timestamp":time().__trunc__(), "origin": request.client.host}


@router.get("/user/{user_id}",tags=["users_db"])
async def get_userid(user_id:str):
    user = get_userdb_handler(user_id)
    return {user_id:user}
