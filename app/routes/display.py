from __future__ import annotations
import os
from fastapi import APIRouter, Depends,Response
from app.routes.images import save_posted_b64img, save_posted_binimg
from pydantic import BaseModel
from app.utils.handler import ImageHandler


router = APIRouter()

class ImageReturn(BaseModel):
    bin_image:bytes

@router.post("/display_uploaded",tags=["face_detection_landmarks"],response_model=ImageReturn, response_class=Response)
def face_detect( image_handle:Depends=Depends(save_posted_binimg)) -> ImageReturn:
    
    return Response(content=image_handle['image_bytes'], media_type='image/png')

@router.post("/b64/display_uploaded",tags=["face_detection_landmarks"],response_model=ImageReturn, response_class=Response)
def face_detect( image_handle:Depends=Depends(save_posted_b64img)) -> ImageReturn:
    
    return Response(content=image_handle['image_bytes'], media_type='image/png')
