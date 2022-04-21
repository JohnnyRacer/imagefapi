import numpy as np
import numpy.matlib
from PIL import Image
import cv2

gen_dummy_image = lambda dimen=(512,512, 3) : (np.random.random_sample(size=dimen)*255).astype('uint8')

color_mode_conv = lambda input_img, conv_type="gray" : cv2.cvtColor(input_img, cv2.COLOR_RGB2GRAY) if conv_type is "gray" else  cv2.cvtColor(input_img, cv2.COLOR_GRAY2RGB)

