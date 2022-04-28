from __future__ import annotations
from fastapi import APIRouter, Depends, File, HTTPException,Form, UploadFile
from pydantic import BaseModel
from app.core.auth import get_current_user
from typing import Optional
from http import HTTPStatus
from hashlib import sha256
from app.utils.handler import ImageHandler
from app.core import config 
import base64 as b64 
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
@router.post("/b64upload",tags=['upload_images'],response_model=ImageUploadResponse)
async def save_posted_b64img(
    b64_image: str = Form(...),
    auth:Depends if bool(int(config.API_AUTH_CFG)) else None = Depends(get_current_user) if bool(int(config.API_AUTH_CFG)) else None,
    output_ext:str = 'png',
    user_uuid: Optional[str] = None,
    save_image: Optional[bool]=False,

) -> ImageUploadResponse:
    img_chars = len(b64_image)
    if img_chars > config.MAX_IMG_SIZE:
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
            filename = f'{config.IMG_SAVE_DIR}/{img_hash}.{output_ext}' if bool(user_uuid) else f'{config.IMG_CACHE_DIR}/{img_hash}.{output_ext}'
         
            ImageHandler.dump_pil(Image.open(io.BytesIO(b64.b64decode(b64_image))),img_path=filename)
            status = 'Saved sucessfully!'
    except Exception as exp:
        status = f'Failed to parse image due to {exp}'
        img_hash = ''
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Failed to parse image due to exception : {exp} ")
    ret_dict = {'upload_status':status,'image_size': img_chars, 'image_hash':raw_imhash}
    if config.RETURN_SAVEFP:
         ret_dict["filename"] = filename if save_image else f'{img_hash}.{output_ext}'
    return ret_dict
    
@router.post("/upload",tags=['upload_images'], response_model=ImageUploadResponse)
async def save_posted_binimg(
    bin_image: UploadFile = File(...),
    auth: Depends if bool(int(config.API_AUTH_CFG)) else None = Depends(get_current_user) if bool(int(config.API_AUTH_CFG)) else None, # Normally the syntax for requiring auth has a type check of 'Depends', ex. (auth : Depends = Depends(get_current_user)), the type anno needs to removed since it interfereres with setting auth to None 
    user_uuid: Optional[str] = None,
    save_image: Optional[bool]=False,    
) -> ImageUploadResponse:
    try:
        not config.DEBUG or print(user_uuid)
        not config.DEBUG or print(type(user_uuid))
        filename = f"{config.IMG_SAVE_DIR if user_uuid is not None else config.IMG_CACHE_DIR}/{bin_image.filename}"
        content = await bin_image.read()
        if len(content) > config.MAX_IMG_SIZE:
            raise HTTPException(
                status_code=HTTPStatus.METHOD_NOT_ALLOWED,
                detail=f"Unalbe to parse uploaded due to image size exceeding limit of : {config.MAX_IMG_SIZE} "
            ) 
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
    ret_dict = {'upload_status':status, 'image_size': img_size, 'image_hash':raw_imhash}
    if config.RETURN_SAVEFP:
         ret_dict["filename"] = filename if save_image else bin_image.filename
    return ret_dict 
