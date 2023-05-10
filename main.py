import time
import os

import RPi.GPIO as GPIO
from picamera import PiCamera

import cv2
import numpy as np
from pytesseract import pytesseract
import pyttsx3

import pygame

def take_picture(pin):
    dir_path = './raw_images'
    counter = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            counter += 1
    camera = PiCamera()
    camera.start_preview()
    # time.sleep(10)
    # camera.capture(f'./raw_images/sample{counter + 1}.jpg')
    # camera.stop_preview()
    # camera.close()
    
    # image2text(f"sample{counter + 1}")

def image2text(imageName):
    # Precprocessing:
    # get grayscale image
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(image):
        return cv2.medianBlur(image,5)
    
    #thresholding (aka convert to binary)
    def thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #dilation
    def dilate(image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.dilate(image, kernel, iterations = 1)
        
    #erosion
    def erode(image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.erode(image, kernel, iterations = 1)

    #opening - erosion followed by dilation
    def opening(image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    #canny edge detection
    def canny(image):
        return cv2.Canny(image, 100, 200)

    #skew correction
    def deskew(image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    #template matching
    def match_template(image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 
    
    # Compare 2 images
    def mse(img1, img2):
        h, w, rgb = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err / float(h * w)
        return mse
    
    raw_img = cv2.imread('./raw_images/' + imageName + '.jpg')
    
    # TODO Read about grayscale and threshold
    processed_img = get_grayscale(raw_img)
    processed_img = thresholding(processed_img)        # Image dimensions are 2 - Height, Width
    cv2.imwrite('./processed_images/new.jpg', processed_img) # Write to an image so that the image dimensions are 3 - Height, Width, RGB
    processed_img = cv2.imread('./processed_images/new.jpg')
    
    existing = False
    dir_path = './processed_images'
    for path in os.listdir(dir_path):
        existing_img = cv2.imread('./processed_images/' + str(os.path.basename(path)))
        if existing_img.shape == processed_img.shape and str(os.path.basename(path)) != "new.jpg":
            error = mse(existing_img, processed_img)
            if error < 5:
                os.remove('./processed_images/new.jpg')
                # os.remove('./raw_images/' + imageName + '.jpg')
                filename = os.path.basename(path)
                filename = os.path.splitext(filename)[0]
                existing = True
                break
            else:
                os.remove('./processed_images/new.jpg')
                cv2.imwrite('./processed_images/' + imageName + '.jpg', processed_img)
                break
    else:
        os.remove('./processed_images/new.jpg')
        cv2.imwrite('./processed_images/' + imageName + '.jpg', processed_img)
    
    if existing == False:
        # Comment the line below if run on Raspberry PI
        # pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

        text = pytesseract.image_to_string(processed_img)

        # Saving the extracted text
        with open('./texts/' + imageName + '.txt', "w+") as file:
            file.write(text)
        
        text2speech(imageName)
    else:
        print(filename)

def text2speech(textName):
    engine = pyttsx3.init()
    
    # The text that you want to convert to audio
    with open('./texts/' + textName + '.txt', "r+") as file:
        text = file.read()

    # Setting voice sound and voice rate
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[11].id) # voices[0] if run on Windows, voices[11] if run on PI
    engine.setProperty("rate", 150)

    # Saving the audio in a wav format
    engine.save_to_file(text, './audio/' + textName + '.wav')

    engine.runAndWait() 

if __name__ == '__main__':
    # Pygame init
    os.environ["DISPLAY"] = ":0"
    pygame.init()
    size = width, height = 320, 240
    screen = pygame.display.set_mode(size)
    
    # Audio condition
    firstPlay = False
    playing = False
    
    
    # Pin Definitions:
    stopPin = 22
    camPin = 17
    audioPin_play = 23
    audioPin_stop = 24
    randomPin = 16

    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

    GPIO.setup(stopPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(camPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(audioPin_play, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(audioPin_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    print("   Smart Reader begins.\n",
          "1. Press button 0 to stop. Hold button 0 to restart PI.\n",
          "2. Press button 1 to take picture.\n",
          "3. Press button 2 to play or pause audio.\n",
          "4. Hold button 2 to stop audio.\n")
    
    while True:
        try:
            if GPIO.input(stopPin) == False:
                time.sleep(2)
                # Check if button is still being hold after 3 seconds
                if GPIO.input(stopPin) == False:
                    GPIO.cleanup()
                    print("Smart Reader has finished.\n")
                    os.system("reboot")
                else:
                    GPIO.cleanup()
                    print("Smart Reader has finished.\n")
                    break
            if GPIO.input(camPin) == False:
                take_picture(GPIO.input(camPin))
                print("Picture taken.\n")
            if GPIO.input(audioPin_play) == False:
                if not firstPlay:
                    pygame.mixer.init()
                    pygame.mixer.music.load('./audio/' + "sample1" + '.wav')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    playing = True
                    firstPlay = True
                else:
                    if playing:
                        pygame.mixer.music.pause()
                        playing = False
                        print("Audio paused.\n")
                        break
                    else:
                        pygame.mixer.music.unpause()
                        playing = True
                        print("Audio played.\n")
                        break
            if GPIO.input(audioPin_stop) == False:
                if firstPlay:
                    pygame.mixer.music.stop()
                    playing = False
                    firstPlay = False
                    print("Audio stopped.\n")
                    break
        except Exception as e:
            print(e)
            break
