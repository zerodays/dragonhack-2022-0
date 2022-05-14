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

        (x, y), freq = process_sequence.process_frame(image, tla)
        if freq > 0:
            s = sounds[y][x].play()
            time.sleep(0.01)

        k = cv2.waitKey(10) & 0XFF

cv2.destroyAllWindows()
