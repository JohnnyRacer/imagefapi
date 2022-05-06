from __future__ import annotations
import os
import shutil
from fastapi import APIRouter, Depends, File, HTTPException,Form, UploadFile
from pydantic import BaseModel
from typing import Optional
from http import HTTPStatus
from hashlib import sha256
from app.utils.handler import ImageHandler
from app.core import config 
import base64 as b64 
import io
from PIL import Image

router = APIRouter()


class ImageUploadResponse(BaseModel):
    upload_status:str # Human friendly message
    filename: str 
    image_size:int
    image_hash:str
    bytes_output:Optional[bytes] = None
    filename: Optional[str] = None

#Union(Depends, None) =
#@router.post("/b64upload",tags=["upload_images"],response_model=ImageUploadResponse)
async def save_posted_b64img(
    b64_image: str = Form(...),
    keep_image:bool = False,
    save_dir: str= None
) -> ImageUploadResponse:
    output_ext = "png"
    img_chars = len(b64_image)
    if img_chars > config.MAX_IMG_SIZE:
        raise HTTPException(
            status_code=HTTPStatus.METHOD_NOT_ALLOWED,
            detail=f"Image exceeds maximum size of 14 megabytes" # Prevent memory overflow attacks on the server by crafted large malicious files
        )
    filename = ''
    try:
        b64_image = b64_image if len(b64_image.split(',')) == 1 else b64_image.split(',')[-1]
        raw_imhash = sha256(b64_image.encode('utf-8')).hexdigest()
        img_hash  = raw_imhash[-32:]            
        filename = f"{save_dir}/{img_hash}.{output_ext}" if save_dir is not None and os.path.isdir(save_dir)  else f'{config.IMG_CACHE_DIR}/{img_hash}.{output_ext}' 
        
        status = 'Recieved sucessfully!'
        content = b64.b64decode(b64_image)
        if keep_image:
            ImageHandler.dump_pil(Image.open(io.BytesIO(content)),img_path=filename)
            status = 'Saved sucessfully!'
    except Exception as exp:
        status = f'Failed to parse image due to {exp}'
        img_hash = ''
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Failed to parse image due to exception : {exp} ")
    ret_dict = {'upload_status':status,'image_size': img_chars, 'image_hash':raw_imhash, "filename":filename,'image_bytes':content}
    return ret_dict
    
#@router.post("/upload",tags=["upload_images"], response_model=ImageUploadResponse)
async def save_posted_binimg(
    bin_image: UploadFile = File(...),
    keep_image:bool = False,
    save_dir: str= None
) -> ImageUploadResponse:
    try:
        filename = f"{save_dir}/{bin_image.filename}" if save_dir is not None and os.path.isdir(save_dir) else f"{config.IMG_CACHE_DIR}/{bin_image.filename}"
        content = await bin_image.read()
        if len(content) > config.MAX_IMG_SIZE:
            raise HTTPException(
                status_code=HTTPStatus.METHOD_NOT_ALLOWED,
                detail=f"Unalbe to parse uploaded due to image size exceeding limit of : {config.MAX_IMG_SIZE} "
            ) 
        raw_imhash = sha256(content).hexdigest()
        img_size = len(content)
        image_bytes = ImageHandler.dump_pil(Image.open(io.BytesIO(content)))
        status = 'Recieved sucessfully!'
        if keep_image:
            status = 'Saved sucessfully!'
            ImageHandler.dump_pil(Image.open(io.BytesIO(content)),img_path=filename )
            
    except Exception as exp:
        status = f'Failed to parse image due to {exp}'
        raw_imhash = ''
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Failed to parse image due to exception : {exp} ")
    ret_dict = {'upload_status':status, 'image_size': img_size, 'image_hash':raw_imhash, 'filename': filename if keep_image else None ,'image_bytes':content}

    return ret_dict 
