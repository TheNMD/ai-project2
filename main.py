from PIL import Image
from pytesseract import pytesseract
import RPi.GPIO as GPIO
import time
import pyttsx3

def image2text(imageName):
    # TODO How tesseract works, how to train tesseract on custom training data
    
    # Comment the line below if run on Raspberry PI
    # pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

    # Opening the image and storing it in an image object
    img = Image.open('./images/' + imageName + '.jpg')

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
    pwmPin = 18 # Broadcom pin 18 (P1 pin 12)
    # ledPin = 23 # Broadcom pin 23 (P1 pin 16)
    butPin = 17 # Broadcom pin 17 (P1 pin 11)

    dc = 95 # duty cycle (0-100) for PWM pin

    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    # GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
    GPIO.setup(pwmPin, GPIO.OUT) # PWM pin set as output
    pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency
    GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
    
    # GPIO.output(ledPin, GPIO.LOW)
    pwm.start(dc)
    print("Press CTRL+C to exit")
    
    try:
        while True:
            if GPIO.input(butPin): # button is released
                print("0")
                time.sleep(1.0)
                # pwm.ChangeDutyCycle(dc)
                # GPIO.output(ledPin, GPIO.LOW)
            else: # button is pressed:
                print("1")
                time.sleep(1.0)
                # pwm.ChangeDutyCycle(100-dc)
                # GPIO.output(ledPin, GPIO.HIGH)
                # time.sleep(0.075)
                # GPIO.output(ledPin, GPIO.LOW)
                # time.sleep(0.075)
    # If CTRL+C is pressed, exit cleanly:
    except KeyboardInterrupt:
        print("-1") 
        pwm.stop() # stop PWM
        GPIO.cleanup() # cleanup all GPIO
    
    # name = "sample1"
    # image2text(name)
    # text2speech(name, play=False)
