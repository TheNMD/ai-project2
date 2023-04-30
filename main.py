from PIL import Image
from pytesseract import pytesseract
import cv2
import numpy as np
import pyttsx3
# import RPi.GPIO as GPIO
# from picamera import PiCamera
import time
import os

def take_picture():
    dir_path = './raw_images'
    counter = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            counter += 1
    camera = PiCamera()
    camera.start_preview()
    time.sleep(3)
    camera.capture(f'./raw_images/sample{counter + 1}.jpg')
    camera.stop_preview()
    camera.close()
    
    image2text(f"sample{1}")

def image2text(imageName):
    # TODO How tesseract works, image preprocessing
    # Precprocessing:
    def get_grayscale(image): pass
    
    # Comment the line below if run on Raspberry PI
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

    # Opening the image and storing it in an image object
    img = Image.open('./raw_images/' + imageName + '.jpg')

    # Passing the image object to image_to_string() function extract the text from the image
    text = pytesseract.image_to_string(img)

    # Saving the extracted text
    with open('./texts/' + imageName + '.txt', "w+") as file:
        file.write(text)
        
    text2speech(imageName, play=False)

def text2speech(textName, play):
    engine = pyttsx3.init("espeak")
    
    # The text that you want to convert to audio
    with open('./texts/' + textName + '.txt', "r+") as file:
        text = file.read()

    # Setting voice sound and voice rate
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[11].id)
    engine.setProperty("rate", 150) # default 200

    # Saving the audio in a wav format
    engine.save_to_file(text, './audio/' + textName + '.wav')

    # Playing the audio
    if play:
        playaudio(textName)

    engine.runAndWait()

def playaudio(audioName):
    # TODO Play, Stop, Playback, ... features
    pass

def button(): pass

if __name__ == '__main__':
    # # Pin Definitons:
    # stopPin = 22
    # camPin = 17
    # audioPin_play = 23
    # randomPin1 = 24
    # randomPin2 = 16
    # # audioPin_skip = 0
    # # audioPin_back = 0
    # # audioPin_speed = 0

    # # Pin Setup:
    # GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    
    # GPIO.setup(stopPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(camPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # print("Smart Reader begins.\n")
    # print("Press button 0 to stop.\n",
    #       "Press button 1 to take picture.\n",
    #       "Press button 2 to play or stop audio.\n")
    # while True:
    #     try:
    #         if GPIO.input(stopPin) == False:
    #             GPIO.cleanup()
    #             print("Smart Reader has finished.\n")
    #             break
    #         if GPIO.input(camPin) == False:
    #             take_picture()
    #             print("Picture taken.\n")
    #     except Exception as e:
    #         print(e)
    #         continue
    
    
    image2text("sample1")
