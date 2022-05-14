#!/usr/bin/env python
from base64 import b64decode

from PIL import Image, ImageOps
from io import BytesIO
import numpy as np
from base64 import b64decode


def read_image(message):

    buf = BytesIO()
    buf.write(message)

    im = Image.open(buf)
    open_cv_image = np.array(im)[:,:,0]

    # open_cv_image = open_cv_image[:,::-1]

    return open_cv_image

def read_sequence(path):
    with open(path) as f:
        lines = f.readlines()
        for message in lines:
            if message.startswith('|||'):
                message = b64decode(message.encode('utf-8'))
                img = read_image(message)
                yield img