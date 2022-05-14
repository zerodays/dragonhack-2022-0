#!/usr/bin/env python
from base64 import b64decode
from email import message
from msilib import sequence
import queue
import time

from PIL import Image, ImageOps
from io import BytesIO
import cv2
import numpy as np
from base64 import b64decode
import sys


def read_image(message):

    buf = BytesIO()
    buf.write(message)

    im = Image.open(buf)
    pil_image = ImageOps.grayscale(im)
    open_cv_image = np.array(pil_image)

    # cv2.imshow('image', open_cv_image)
    # k = cv2.waitKey()
    return open_cv_image

def read_sequence():
    sequence = []
    with open('test') as f:
        lines = f.readlines()
        for message in lines:
            if message.startswith('|||'):
                message = b64decode(message.encode('utf-8'))
                img = read_image(message)
                sequence.append(img)

    return sequence

read_sequence()

# cv2.destroyAllWindows()