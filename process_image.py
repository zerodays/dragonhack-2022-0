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
import matplotlib.pyplot as plt

def process_image(message):

    buf = BytesIO()
    buf.write(message)

    im = Image.open(buf)
    open_cv_image = np.array(im)

    cv2.imshow('image0', open_cv_image)


while True:
    message = input()
    if message.startswith('|||'):

        try:
            message = b64decode(message.encode('utf-8'))
        except BrokenPipeError:
            continue

        process_image(message)
        k = cv2.waitKey(10) & 0XFF

cv2.destroyAllWindows()
