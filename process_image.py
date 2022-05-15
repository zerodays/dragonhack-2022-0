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
from python_audio import read_sequence
from python_audio import process_sequence
from pydub.playback import play
from threading import Thread

tla = read_sequence.read_sequence("tla").__next__()

sounds = process_sequence.read_sounds()

while True:
    message = input()    
    
    if message.startswith('|||'):

        try:
            message = b64decode(message.encode('utf-8'))
        except BrokenPipeError:
            continue

        image = read_sequence.read_image(message)

        (x, y), white_confidence = process_sequence.process_frame(image, tla)
        white_confidence -= 0.2
        white_confidence *= 1/0.7
        white_confidence = max(0, min(1, white_confidence))
        za_utisat = (1 - white_confidence) * 20

        if white_confidence > 0:
            s = sounds[y][x]
            s -= za_utisat
            Thread(target=lambda: play(s)).start()
            time.sleep(0.01)

cv2.destroyAllWindows()
