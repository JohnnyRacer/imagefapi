import re
import base64 as b64
import io
from PIL import Image
from requests import request
import requests
from skimage import io as skio
import numpy as np

class ImageHandler:

    def dump_pil(in_image:Image,fmt='png',img_path:str=None) -> bytes:

        with open(img_path, 'wb') if img_path != None and bool(img_path) else io.BytesIO() as wfp:
            try:
                in_image.save(wfp, fmt)
                ret_bytes = None
                if img_path == None:
                    wfp.seek(0)
                    ret_bytes = wfp.read()
            except Exception as exp:
                pass

            return ret_bytes

    bytes_toimage = lambda in_bytes : Image.open(io.BytesIO(in_bytes))

    decode_b64img = lambda in_b64im, ret_ndarray=False : Image.frombuffer(b64.b64decode(in_b64im)) if ret_ndarray else Image.frombuffer(b64.b64decode(in_b64im))

    encode_bytesb64 = lambda in_bytes : b64.b64decode(in_bytes)

    def image_puller(im_fpurl:str,method="ski") -> np.ndarray:
        if method == "ski":
            ret_image = skio.imread(im_fpurl)
        elif method == "req":
            ret_image = np.array(Image.open(io.BytesIO(requests.get(im_fpurl).content)))
        return ret_image

    def base64_to_image(base64_str : str) -> Image:
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = b64.b64decode(base64_data)
        return ImageHandler.bytes_toimage(byte_data)
