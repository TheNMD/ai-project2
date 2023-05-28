import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["DISPLAY"] = ":0"

import RPi.GPIO as GPIO
from picamera import PiCamera

import cv2
from imutils import resize
from transform import perspective_transform
from pytesseract import pytesseract

import pyttsx3
import pygame

def imageProcessing(imageName):
    def findDoc(contours):
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                return approx
        return None
    
    original_img = cv2.imread(f'./raw_images/{imageName}.jpg')
    copy = original_img.copy()

    ratio = original_img.shape[0] / 500.0
    resized_img = resize(original_img, height=500)
    gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
    edged_img = cv2.Canny(blurred_img, 75, 200)
    
    contours, _ = cv2.findContours(edged_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    doc = findDoc(contours)
    if doc is None:
        return "errorContour"
    for corner in doc:
        tuple_point = tuple(corner[0])
        cv2.circle(resized_img, tuple_point, 3, (0, 0, 255), 4)
    
    warped_img = perspective_transform(copy, doc.reshape(4, 2) * ratio)
    warped_img = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)
    ret, thresh_img = cv2.threshold(warped_img, 120, 255, cv2.THRESH_BINARY)
    
    cv2.imwrite(f'./processed_images/{imageName}.jpg', thresh_img)
    
    return image2text(imageName, warped_img)

def image2text(imageName, img):
    # Comment the line below if run on Raspberry PI
    # pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

    text = pytesseract.image_to_string(img)

    with open(f'./texts/{imageName}.txt', "w+") as file:
        file.write(text)
        
    return text2speech(imageName, text)

def text2speech(textName, text):
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[11].id) # voices[0] if run on Windows, voices[11] if run on PI
    engine.setProperty("rate", 150)

    engine.save_to_file(text, f'./audio/{textName}.wav')

    engine.runAndWait()
    
    return textName 

if __name__ == '__main__':
    # Pygame init
    pygame.init()
    screen = pygame.display.set_mode((1,1))
    pygame.mixer.init()
    
    # Audio condition
    firstPlay = False
    playing = False
    filename =  "" # imageProcessing("sample2")
    
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
    
    pygame.mixer.music.load(f'./audio/default/begin.wav')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    
    while True:
        if GPIO.input(stopPin) == False:
            time.sleep(0.25)
            if playing:
                pygame.mixer.music.stop()
                playing = False
                firstPlay = False
            GPIO.cleanup()
            print("Smart Reader has finished.\n")
            pygame.mixer.music.load(f'./audio/default/finish.wav')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            time.sleep(1.5)
            break
        if GPIO.input(camPin) == False:
            time.sleep(0.25)
            if playing:
                print("Stop audio first.\n")
                continue
            dir_path = './raw_images'
            counter = 0
            for path in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, path)):
                    counter += 1
            camera = PiCamera()
            camera.start_preview()
            print("Ready to take picture.\n")
            pygame.mixer.music.load(f'./audio/default/ready.wav')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            # time.sleep(1)
            while True:
                if GPIO.input(camPin) == False:
                    break
            camera.capture(f'./raw_images/sample{counter + 1}.jpg')
            camera.stop_preview()
            camera.close()
            filename = imageProcessing(f"sample{counter + 1}")
            if filename == "errorContour":
                print("Error: Contour.\n")
                pygame.mixer.music.load(f'./audio/default/errorContour.wav')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
            else:
                print("Picture taken.\n")
                pygame.mixer.music.load(f'./audio/default/pictureTaken.wav')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
        if GPIO.input(audioPin_play) == False:
            time.sleep(0.25)
            if not firstPlay:
                if filename == "":
                    print("No picture chosen.\n")
                    continue
                pygame.mixer.music.load(f'./audio/{filename}.wav')
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
            time.sleep(0.25)
            if firstPlay:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(f'./audio/{filename}.wav')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                playing = True
                print("Audio replayed.\n")
            else:
                print("No audio is playing.\n")         
        if GPIO.input(audioPin_stop) == False:
            time.sleep(0.25)
            if firstPlay:
                pygame.mixer.music.stop()
                playing = False
                firstPlay = False
                print("Audio ended.\n")
            else:
                print("No audio is playing.\n") 
