from __future__ import annotations
from base64 import b64decode

from fastapi import APIRouter, Depends, File, HTTPException,Form,Body, UploadFile
from pydantic import BaseModel
from app.core.auth import get_current_user
from typing import Any, Optional, Union
from http import HTTPStatus
from hashlib import sha256, md5, blake2b,sha384
from app.utils.handler import ImageHandler
from app.core.config import IMG_CACHE_DIR, IMG_SAVE_DIR,API_AUTH_CFG
import io
from PIL import Image


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
    upload_status:str # Human friendly message
    filename: str 
    image_size:int
    image_hash:str
    filename: Optional[str] = None

#Union(Depends, None) =
@router.post("/b64upload",tags=['upload_images'])
async def save_posted_b64img(
    b64_image: str = Form(...),
    auth= Depends(get_current_user) if bool(int(API_AUTH_CFG)) else None,
    output_ext:str = 'png',
    user_uuid: Optional[str] = None,
    save_image: Optional[bool]=False,
    
) -> dict[str, Any]:
    img_chars = len(b64_image)
    if img_chars > 14000000:
        raise HTTPException(
            status_code=HTTPStatus.METHOD_NOT_ALLOWED,
            detail=f"Image exceeds maximum size of 14 megabytes" # Prevent memory overflow attacks on the server by crafted large malicious files
        )
    try:
        b64_image = b64_image if len(b64_image.split(',')) == 1 else b64_image.split(',')[-1]
        raw_imhash = sha256(b64_image.encode('utf-8')).hexdigest()
        img_hash  = raw_imhash[-32:]
        status = "Recieved sucessfully!"
        if save_image:

            filename = f'{IMG_SAVE_DIR}/{img_hash}.{output_ext}' if bool(user_uuid) else f'{IMG_CACHE_DIR}/{img_hash}.{output_ext}'
            #ImageHandler.dump_pil(Image.open(io.BytesIO(b64decode(b64_image))),img_path=filename)
            ImageHandler.dump_pil(Image.open(io.BytesIO(b64decode(b64_image))),img_path=filename)
            status = 'Saved sucessfully!'
    except Exception as exp:
        status = f'Failed to parse image due to {exp}'
        img_hash = ''
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Failed to parse image due to exception : {exp} ")

    return {'message':status,'image_size': img_chars, 'img_hash':raw_imhash, "filename":filename if save_image else f'{img_hash}.{output_ext}' }
    
@router.post("/upload",tags=['upload_images'],response_model=ImageUploadResponse)
async def save_posted_binimg(
    bin_image: UploadFile = File(...),
    auth= Depends(get_current_user) if bool(int(API_AUTH_CFG)) else None, # Normally the syntax for requiring auth has a type check of 'Depends', ex. (auth : Depends = Depends(get_current_user)), the type anno needs to removed since it interfereres with setting auth to None 
    user_uuid: Optional[str] = None,
    save_image: Optional[bool]=False,
    
    
):
    try:
        print(user_uuid)
        print(type(user_uuid))
        filename = f"{IMG_SAVE_DIR if user_uuid is not None else IMG_CACHE_DIR}/{bin_image.filename}"
        content = await bin_image.read()
        raw_imhash = sha256(content).hexdigest()
        img_size = len(content)
        status = 'Recieved sucessfully!'
        if save_image:
            print(f"Saved to {filename} ")
            ImageHandler.dump_pil(Image.open(io.BytesIO(content)),img_path=filename)
            status = 'Saved sucessfully!'
    except Exception as exp:
        status = f'Failed to parse image due to {exp}'
        raw_imhash = ''
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Failed to parse image due to exception : {exp} ")
    return {'message':status, 'filename':bin_image.filename, 'image_size': img_size, 'img_hash':raw_imhash, "filename":filename if save_image else '' }
