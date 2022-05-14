#!/usr/bin/env python
from base64 import b64decode
from email import message
import queue
import time

from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from base64 import b64decode


def process_image(message):

    buf = BytesIO()
    buf.write(message)

    im = Image.open(buf)
    pil_image = im.convert('RGB') 
    open_cv_image = np.array(pil_image) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    cv2.imshow('image', open_cv_image)

while True:
    message = input()
    if message.startswith('|||'):
        message = b64decode(message.encode('utf-8'))
        process_image(message)
        k = cv2.waitKey(10) & 0XFF

cv2.destroyAllWindows()
