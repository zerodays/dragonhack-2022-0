import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import time 
from read_sequence import read_sequence

import simpleaudio as sa

def read_sounds():
    folder = "./sounds"
    tags_vertical = ["low", "mid", "high"]
    tags_horizontal = ["50L", "25L", "C", "25R", "50R"]

    sounds = []

    for vtag in tags_vertical:
        row = []
        for htag in tags_horizontal:
            path = os.path.join(folder, "beep_" + vtag + "_" + htag + ".wav")
            wave_obj = sa.WaveObject.from_wave_file(path)
            row.append(wave_obj)
        sounds.append(row)

    return sounds


def process_frame(img, H_REGIONS=5, V_REGIONS=3):
    img_size = img.shape[:2]

    cv2.imshow('image', img)
    k = cv2.waitKey()

    n_regions_h = int(img_size[1] // H_REGIONS)
    n_regions_v = int(img_size[0] // V_REGIONS)

    regions_x = []
    regions_y = []

    for hi in range(H_REGIONS):
        region = img[hi * n_regions_h: (hi + 1) * n_regions_h, :]
        mean = np.mean(region) / 255
        regions_x.append(mean)

    for vi in range(V_REGIONS):
        region = img[:, vi * n_regions_v: (vi + 1) * n_regions_v]
        mean = np.mean(region) / 255
        regions_y.append(mean)

    x, y = np.argmin(regions_x), np.argmin(regions_y)

    freq = round(5 / max(min(regions_x[x], regions_y[y]), 0.5))

    return (x, y), freq
    

sounds = read_sounds()
sequence = read_sequence()

for frame in sequence:
    (x, y), freq = process_frame(frame)
    s = sounds[y][x].play()
    time.sleep(1 / freq)
