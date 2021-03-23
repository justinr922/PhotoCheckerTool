import msvcrt
import os
from PIL import Image
import subprocess
from pynput import keyboard
import cv2
import matplotlib.pyplot as plt
import sys
from pathlib import Path

def photolist():
    _iterator = 0
    while True:
        yield sorted(os.listdir(os.getcwd()))[_iterator]
        _iterator += 1

def on_press(key):
    global input
    try:
        if key == keyboard.Key.esc:
            input = key
            plt.close('all')
        elif key.char == 'y':
            print('This image meets criteria.')
            input = key.char
            plt.close('all')
        elif key.char == 'n':
            print('Not relevant.')
            input = key.char
            plt.close('all')
        elif key.char == 'r':
            input = key.char
    except:
        pass

def on_release(key):
    pass
    #global _x
    #_x = key

OUTPUT_DIR = Path(os.getcwd()) / 'Yes'
IGNORE_DIR = Path(os.getcwd()) / 'No'

if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
if not os.path.isdir(IGNORE_DIR):
    os.mkdir(IGNORE_DIR)

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
#plt.ion()
for i, photo in enumerate(sorted(os.listdir(os.getcwd()))):
    if photo[-3:].lower() == 'jpg':
        print(f'Displaying {photo}')
        while True:
            try:
                input = ''
                img = cv2.imread(photo)
                cv2.namedWindow(photo)
                cv2.moveWindow(photo, 0,0)
                scale_percent = 40 # percent of original size
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
                dim = (width, height)
                img = cv2.resize(img, dim)
                cv2.imshow(photo, img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                if input == keyboard.Key.esc:
                    print('Exiting.....')
                    sys.exit()
                elif input == 'y':
                    os.replace(photo, OUTPUT_DIR / photo)
                    last_photo = OUTPUT_DIR / photo
                    break
                elif input == 'n':
                    os.replace(photo, IGNORE_DIR / photo)
                    last_photo = IGNORE_DIR / photo
                    break
                elif input == 'r':
                    try:
                        print(last_photo)
                        os.replace(last_photo, str(last_photo).split('\\')[-1])
                        print("Undoing last move...")

                    except Exception as  e:
                        print(e)
                        #rint("File not found.")

            except SystemExit:
                sys.exit()
