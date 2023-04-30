from PIL import Image
from pytesseract import pytesseract
import pyttsx3
import RPi.GPIO as GPIO
from picamera import PiCamera
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
    print(f"Picture taken: sample{counter + 1}")

def image2text(imageName):
    # TODO How tesseract works, how to train tesseract on custom training data
    
    # Comment the line below if run on Raspberry PI
    # pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

    # Opening the image and storing it in an image object
    img = Image.open('./raw_images/' + imageName + '.jpg')

    # Passing the image object to image_to_string() function extract the text from the image
    text = pytesseract.image_to_string(img)

    # Saving the extracted text
    with open('./texts/' + imageName + '.txt', "w+") as file:
        file.write(text)

def text2speech(textName, play):
    engine = pyttsx3.init()
    
    # The text that you want to convert to audio
    with open('./texts/' + textName + '.txt', "r+") as file:
        text = file.read()

    # Setting voice sound and voice rate
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id) # voices[0]
    engine.setProperty("rate", 175) # default 200

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
    # Pin Definitons:
    stopPin = 2
    camPin = 17
    audioPin_play = 23
    audioPin_stop = 24
    audioPin_replay = 16
    # audioPin_skip = 0
    # audioPin_back = 0
    # audioPin_speed = 0

    # dc = 95 # duty cycle (0-100) for PWM pin

    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    # GPIO.setup(pwmPin, GPIO.OUT) # PWM pin set as output
    # pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency
    
    GPIO.setup(stopPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(camPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # pwm.start(dc)

    # Pin Setup - Broadcom pin-numbering scheme:
    GPIO.setmode(GPIO.BCM)
    
    print("Smart Reader begins.")
    while True:
        if GPIO.input(stopPin) == False:
            GPIO.cleanup()
            print("Smart Reader has finished.")
            break
        if GPIO.input(camPin) == False:
            take_picture()
            time.sleep(1.0)

