import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["DISPLAY"] = ":0"
import RPi.GPIO as GPIO
from picamera import PiCamera
import cv2
import numpy as np
from pytesseract import pytesseract
import pyttsx3
import pygame

def take_picture():
    dir_path = './raw_images'
    counter = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            counter += 1
    camera = PiCamera()
    camera.start_preview()
    # time.sleep(2)
    # camera.capture(f'./raw_images/sample{counter + 1}.jpg')
    # camera.stop_preview()
    # camera.close()
    
    # return image2text(f"sample{counter + 1}")

def image2text(imageName):
    # Preprocessing:
    # get grayscale image
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(image):
        return cv2.medianBlur(image,5)
    
    # Thresholding (convert to binary)
    def thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Compare 2 images
    def mse(img1, img2):
        h, w, rgb = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err / float(h * w)
        return mse
    
    raw_img = cv2.imread(f'./raw_images/{imageName}.jpg')
    
    # TODO Read about grayscale and threshold
    processed_img = get_grayscale(raw_img)
    processed_img = thresholding(processed_img) # Image dimensions are 2 - Height, Width
    cv2.imwrite('./processed_images/new.jpg', processed_img) # Write to an image so that the image dimensions are 3 - Height, Width, RGB
    processed_img = cv2.imread('./processed_images/new.jpg')
    
    existing = False
    dir_path = './processed_images'
    for path in os.listdir(dir_path):
        existing_img = cv2.imread(f'./processed_images/{os.path.basename(path)}')
        if existing_img.shape == processed_img.shape and str(os.path.basename(path)) != "new.jpg":
            error = mse(existing_img, processed_img)
            if error < 5:
                os.remove('./processed_images/new.jpg')
                # os.remove(f'./raw_images/{imageName}.jpg)
                filename = os.path.basename(path)
                filename = os.path.splitext(filename)[0]
                existing = True
                break
            else:
                os.remove('./processed_images/new.jpg')
                cv2.imwrite(f'./processed_images/{imageName}.jpg', processed_img)
                break
    else:
        os.remove('./processed_images/new.jpg')
        cv2.imwrite(f'./processed_images/{imageName}.jpg', processed_img)
    
    if existing == False:
        # Comment the line below if run on Raspberry PI
        # pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

        text = pytesseract.image_to_string(processed_img)

        # Saving the extracted text
        with open(f'./texts/{imageName}.txt', "w+") as file:
            file.write(text)
        
        return text2speech(imageName)
    else:
        return filename

def text2speech(textName):
    engine = pyttsx3.init()
    
    # The text that you want to convert to audio
    with open(f'./texts/{textName}.txt', "r+") as file:
        text = file.read()

    # Setting voice sound and voice rate
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[11].id) # voices[0] if run on Windows, voices[11] if run on PI
    engine.setProperty("rate", 150)

    # Saving the audio in a mp3 format
    engine.save_to_file(text, f'./audio/{textName}.mp3')

    engine.runAndWait()
    
    return textName 

if __name__ == '__main__':
    # Pygame init
    pygame.init()
    size = width, height = 320, 240
    screen = pygame.display.set_mode(size)
    
    # Audio condition
    firstPlay = False
    playing = False
    filename = "sample2"
    
    
    # Pin Definitions:
    stopPin = 22
    camPin = 17
    audioPin_play = 23
    audioPin_replay = 24
    audioPin_stop = 16

    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

    GPIO.setup(stopPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(camPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(audioPin_play, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(audioPin_replay, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(audioPin_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    print(" #. Smart Reader begins.\n",
          "1. Press button 1 to stop.\n",
          "2. Press button 2 to take picture.\n",
          "3. Press button 3 to play or pause audio.\n",
          "4. Press button 4 to replay audio.\n",
          "5. Press button 5 to stop audio.\n")
    
    while True:
        try:
            if GPIO.input(stopPin) == False:
                time.sleep(0.5)
                if playing:
                    pygame.mixer.music.stop()
                    playing = False
                    firstPlay = False
                GPIO.cleanup()
                print("Smart Reader has finished.\n")
                break
            if GPIO.input(camPin) == False:
                filename = take_picture()
                print("Picture taken.\n")
            if GPIO.input(audioPin_play) == False:
                time.sleep(0.5)
                if not firstPlay:
                    if filename == "":
                        print("No picture chosen.\n")
                        continue
                    pygame.mixer.init()
                    pygame.mixer.music.load(f'./audio/{filename}.mp3')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()
                    playing = True
                    firstPlay = True
                    print("Audio played.\n")
                else:
                    if playing:
                        pygame.mixer.music.pause()
                        playing = False
                        print("Audio stopped.\n")
                    else:
                        pygame.mixer.music.unpause()
                        playing = True
                        print("Audio played.\n")
            if GPIO.input(audioPin_replay) == False:
                time.sleep(0.5)
                if firstPlay:
                    pygame.mixer.music.rewind()
                    pygame.mixer.music.unpause()
                    playing = True
                    print("Audio replayed.\n")
                else:
                   print("No audio is playing.\n")         
            if GPIO.input(audioPin_stop) == False:
                time.sleep(0.5)
                if firstPlay:
                    pygame.mixer.music.stop()
                    playing = False
                    firstPlay = False
                    print("Audio ended.\n")
                else:
                   print("No audio is playing.\n") 
        except Exception as e:
            print(e)
            break
