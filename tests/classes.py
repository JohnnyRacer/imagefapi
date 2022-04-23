import requests
import numpy as np
import numpy.matlib
from PIL import Image
import cv2
import dhash
import base64 as b64
from app.utils.handler import *
import dotenv



gen_dummy_image = lambda dimen=(512,512, 3) : (np.random.random_sample(size=dimen)*255).astype('uint8')

def gen_hash_pil (in_imgpil):
    row, col = dhash.dhash_row_col(in_imgpil)
    output_hash = dhash.format_bytes(row, col).hex()
    return output_hash

color_mode_conv = lambda input_img, conv_type="gray" : cv2.cvtColor(input_img, cv2.COLOR_RGB2GRAY) if conv_type is "gray" else  cv2.cvtColor(input_img, cv2.COLOR_GRAY2RGB)

class BaseTest:

    auth_proto = lambda username, password,access_token=None: if access_token is None else {''}
    
    post_req = lambda url,post_data=None, post_json=None : requests.post(url,data=post_data, json=post_json)

    get_req = lambda url, payload=None : requests.get(url,params=payload)

    def hash_verif(send_b64=False): #Send a randomly generated image and its hash along with a post request to the endpoint
        image = Image.fromarray(gen_dummy_image())
        image_hash = gen_hash_pil(image)
        image_payload = b64.b64encode(ImageHandler.dump_pil(image)) if send_b64 else ImageHandler.dump_pil(image)
        req = {
            
        } 
        #BaseTest.post_req()
        pass
    

    
