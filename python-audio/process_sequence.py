import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import time 
from read_sequence import read_sequence

import simpleaudio as sa

THRESHOLD = 0.95

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


def process_frame(img,tla, H_REGIONS=10, V_REGIONS=10):
    img = -img.astype(int) + tla.astype(int)
    img_size = img.shape[:2]

    img_displ = np.zeros(img.shape)
    img_displ[img > 0] = img[img > 0]
    cv2.imshow('image', img_displ.astype(np.uint8))
    k = cv2.waitKey(50)

    n_regions_h = int(img_size[1] // H_REGIONS)
    n_regions_v = int(img_size[0] // V_REGIONS)

    regions_x = []
    regions_y = []

    for hi in range(H_REGIONS):
        region = img[:, hi * n_regions_h: (hi + 1) * n_regions_h]
        # print(f"region1: {region.shape}")
        mean = np.mean(region) / 255
        regions_x.append(mean)

    for vi in range(V_REGIONS):
        region = img[vi * n_regions_v: (vi + 1) * n_regions_v, :]
        # print(f"region2: {region.shape}")
        mean = np.mean(region) / 255
        regions_y.append(mean)

    x, y = np.argmin(regions_x), np.argmin(regions_y)

    # print(f"x: {x}, y: {y}")

    # print(f"Regions_X: {regions_x}")
    # print(f"Regions_y: {regions_y}")
    white_confidence = min(regions_x[x], regions_y[y])

    # if no obstacles, we return 0
    if white_confidence > THRESHOLD:
        return (0,0), 0    
    freq = round(5 / max(white_confidence, 0.5))

    return (x*5//H_REGIONS, y*3//V_REGIONS), freq
    

sounds = read_sounds()
sequence = read_sequence("sprehod")

tla = read_sequence("../tla").__next__()


for frame in sequence:
    (x, y), freq = process_frame(frame, tla)
    if freq > 0:
        s = sounds[y][x].play()
        time.sleep(0.01)
