from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException,Form,Body, UploadFile
from pydantic import BaseModel
from app.core.auth import get_current_user
from typing import Any, Optional, Union
from http import HTTPStatus
from hashlib import sha256, md5, blake2b,sha384
from app.utils.handler import ImageHandler

IMG_SAVE_DIR = '/tmp/user_images'
IMG_CACHE_DIR = '/tmp/img_api_cache'
IMG_HASH_METHOD = 'sha2'

router = APIRouter()

class BasicAuthed:
    user_uuid: str # Unique user identifier
    username: str # Human friendly username
    access_token: str  # Using access token provided by jwt to verify, will error out if invalid

class ImageUpload(BaseModel):
    image_b64: str
    img_uuid: str
    img_name: Optional[str] = None
    checksum: Optional[str] = None
    
class ImageURL(BaseModel):
    image_url: str
    upload_action: int # Defines what the server should do with the fetched image
    img_name: Optional[str] = None

class AuthedImageURL(ImageURL, BasicAuthed):
    user_img_uuid: str

class AuthedImageUpload(ImageUpload, BasicAuthed):
    user_img_uuid: str

class ImageUploadResponse(BaseModel):
    upload_message:str # Human friendly message
    image_hash:str
    image_size:int
    filename: Optional[str] = None


@router.post("/b64upload",tags=['upload_images'],response_model=ImageUploadResponse)
async def save_posted_b64img(
    b64_image: str = Form(...),
    user_uuid: Optional[str] = Form(...)
) -> dict[str, Any]:
    img_chars = len(b64_image)
    if img_chars > 14000000:
        raise HTTPException(
            status_code=HTTPStatus.METHOD_NOT_ALLOWED,
            detail=f"Image exceeds maximum size of 14 megabytes" # Prevent memory overflow attacks on the server by crafted large malicious files
        )
    try:
        raw_imhash = sha256(b64_image.encode('utf-8')).hexdigest()
        img_thash  = raw_imhash[-32:]
        img_svfp = f'{IMG_SAVE_DIR}/{img_thash}.png' if bool(user_uuid) else f'{IMG_CACHE_DIR}/{img_thash}.png'
        ImageHandler.dump_pil(b64_image, image_path=img_svfp ) #Dumps 
        status = 'success'
    except Exception as exp:
        status = f'Failed to save due to {exp}'
        img_thash = ''
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Unable to parse image due to exception : {exp} ")

    return {'message':status, 'filename':img_svfp, 'image_size': img_chars, 'img_hash':raw_imhash }

@router.post("/upload",tags=['upload_images'],response_model=ImageUploadResponse)
async def save_posted_binimg(
    bin_image: UploadFile = File(...),
    user_uuid: Optional[str] = Form(...)
):

filename = f" "

"""
@router.post("/url",tags=['pull_image'])
async def save_posted_img(
    form_data }
    
) -> dict[str, Any]:

"""