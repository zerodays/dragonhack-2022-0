#!/usr/bin/env python
from base64 import b64decode
from email import message
import json
import mimetypes
import queue
import time
from base64 import b64encode
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from base64 import b64decode
import matplotlib.pyplot as plt
from python_audio import read_sequence
from python_audio import process_sequence
from pydub.playback import play
from threading import Thread
from math import atan2
from io import BytesIO

tla = read_sequence.read_sequence("tla").__next__()

sounds = process_sequence.read_sounds()

stairs_sound = process_sequence.get_stairs_sound()

while True:
    message = input()    
    
    if message.startswith('|||'):

        try:
            message = b64decode(message.encode('utf-8'))
        except BrokenPipeError:
            continue

        image = read_sequence.read_image(message)

        (x, y), white_confidence, img_displ, peak, valley_confidence = process_sequence.process_frame(image, tla)
        if valley_confidence > 0:
            s = stairs_sound
            Thread(target=lambda: play(s)).start()
            time.sleep(0.01)
        else:
            white_confidence -= 0.2
            white_confidence *= 1/0.7
            white_confidence = max(0, min(1, white_confidence))
            za_utisat = (1 - white_confidence) * 20

            if white_confidence > 0:
                s = sounds[y][x]
                s -= za_utisat
                Thread(target=lambda: play(s)).start()
                time.sleep(0.01)

        px, py = peak
        px -= image.shape[1] // 2
        py -= image.shape[0] // 2


        # Message for server
        buffered = BytesIO()
        Image.fromarray(img_displ).convert('L').save(buffered, format="png")
        img_str = b64encode(buffered.getvalue())
        message = json.dumps({
            'image': img_str.decode('utf-8'),
            'angle': atan2(py, px),
            'intensity': white_confidence
        })

        # print('|||', b64encode(message.encode('utf-8')).decode('utf-8'))


cv2.destroyAllWindows()
