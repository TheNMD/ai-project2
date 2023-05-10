import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["DISPLAY"] = ":0"
import cv2
import numpy as np
from pytesseract import pytesseract
import pyttsx3
import pygame

def image2text(imageName):
    # Preprocessing:
    
    img = cv2.imread(f'./processed_images/{imageName}.jpg')

    
    # Comment the line below if run on Raspberry PI
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

    text = pytesseract.image_to_string(img)

    # Saving the extracted text
    with open(f'./texts/{imageName}.txt', "w+") as file:
        file.write(text)
    
    return text2speech(imageName)

def text2speech(textName):
    engine = pyttsx3.init()
    
    # The text that you want to convert to audio
    with open(f'./texts/{textName}.txt', "r+") as file:
        text = file.read()

    # Setting voice sound and voice rate
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id) # voices[0] if run on Windows, voices[11] if run on PI
    engine.setProperty("rate", 150)

    # Saving the audio in a mp3 format
    engine.save_to_file(text, f'./audio/{textName}.mp3')

    engine.runAndWait()
    
    return textName

image2text("sample8") 