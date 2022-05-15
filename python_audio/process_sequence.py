import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import time 
from python_audio.read_sequence import read_sequence
from scipy.ndimage.filters import gaussian_filter
from pydub import AudioSegment

THRESHOLD = 0.25

THRESHOLD_STAIRS = 0.3

def get_stairs_sound():
    folder = "python_audio/sounds"
    return AudioSegment.from_wav(os.path.join(folder, "stairs.wav"))

def read_sounds():
    folder = "python_audio/sounds"
    tags_vertical = ["low", "mid", "high"]
    tags_horizontal = ["50L", "25L", "C", "25R", "50R"]

    sounds = []

    for vtag in tags_vertical:
        row = []
        for htag in tags_horizontal:
            path = os.path.join(folder, "beep_" + vtag + "_" + htag + ".wav")
            wave_obj = AudioSegment.from_wav(path)
            row.append(wave_obj)
        sounds.append(row)

    return sounds

def process_frame(img, tla):
    img = img.astype(int) - tla.astype(int)

    img_displ = np.zeros(img.shape)
    img_displ[img > 0] = img[img > 0]

    img_negative = np.zeros(img.shape)
    img_negative[img < 0] = img[img < 0]
    img_negative = np.absolute(img_negative)

    blurred = gaussian_filter(img, sigma=7)

    argmax = np.argmax(blurred)
    peak = np.unravel_index(argmax, np.array(blurred).shape)
    peak_value = blurred[peak[0], peak[1]] / 255

    # get lowest point (possibly stairs)
    argmin = np.argmin(blurred)
    valley = np.unravel_index(argmin, np.array(blurred).shape)
    valley_value = abs(blurred[valley[0], valley[1]]) / 255


    # if not valley_value < THRESHOLD:
    #     img_negative = cv2.circle(img_negative, valley[::-1], radius=5, color=(0, 0, 255), thickness=2)
    
    # cv2.imshow('processed', img_negative.astype(np.uint8))
    # k = cv2.waitKey(10)


    if not peak_value < THRESHOLD:
        img_displ = cv2.circle(img_displ, peak[::-1], radius=5, color=(0, 0, 255), thickness=2)
    
    cv2.imshow('processed', img_displ.astype(np.uint8))
    k = cv2.waitKey(10)

    if peak_value < THRESHOLD and valley_value < THRESHOLD_STAIRS:
        return (0,0), 0, img_displ, (0, 0), 0
    
    x_valley, y_valley = valley[::-1]
    if valley_value < THRESHOLD_STAIRS or y_valley < 0.5*img.shape[0]:
        valley_value = 0

    h, w = img.shape
    x, y = peak[::-1]

    h_region =  x * 5 // w
    v_region = y * 3 // h

    return (h_region, v_region), peak_value, img_displ, (x, y), valley_value


def process_frame_old(img,tla, H_REGIONS=10, V_REGIONS=10):
    img = img.astype(int) - tla.astype(int)
    img_size = img.shape[:2]

    img_displ = np.zeros(img.shape)
    img_displ[img > 0] = img[img > 0]
    cv2.imshow('image', img_displ.astype(np.uint8))
    k = cv2.waitKey(10)

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

    x, y = np.argmax(regions_x), np.argmax(regions_y)

    # print(f"x: {x}, y: {y}")

    # print(f"Regions_X: {regions_x}")
    # print(f"Regions_y: {regions_y}")
    white_confidence = max(regions_x[x], regions_y[y])

    # if no obstacles, we return 0
    if white_confidence < THRESHOLD:
        return (0,0), 0    
    # freq = round(5 / max(white_confidence, 0.5))

    return (x*5//H_REGIONS, y*3//V_REGIONS), white_confidence
    

if __name__ == '__main__':
    sounds = read_sounds()

    sequence = read_sequence("../sprehod")
    tla = read_sequence("../tla").__next__()

    for frame in sequence:
        (x, y), freq = process_frame(frame, tla)
        if freq > 0:
            s = sounds[y][x].play()
            time.sleep(0.01)
