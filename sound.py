import time
from openal import * 

SLEEP_TIME = 0.01
N = 100
R = 10

if __name__ == "__main__":
    x_pos = 5
    source = oalOpen("Soft Piano Music_16000_mono.wav")
    source.set_position([0, 0, 0])
    source.set_looping(True)
    source.play()
    listener = Listener()
    listener.set_position([0, 0, 0])

    while True:
        for i in range(-N, N + 1):
            x = i / N
            y = (1 - x ** 2) ** 0.5
            source.set_position([R * x, 0, R * y])
        
            time.sleep(SLEEP_TIME)

        for i in range(N, -N - 1, -1):
            x = i / N
            y = (1 - x ** 2) ** 0.5
            source.set_position([R * x, 0, R * y])
        
            time.sleep(SLEEP_TIME)
    
    oalQuit()