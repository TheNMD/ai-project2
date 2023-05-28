import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["DISPLAY"] = ":0"

import pyttsx3
import pygame

def text2speech(textName, text):
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id) # voices[0] if run on Windows, voices[11] if run on PI
    engine.setProperty("rate", 150)

    engine.save_to_file(text, f'./audio/default/{textName}.wav')

    engine.runAndWait()
    
    return textName

with open(f'./texts/default/noAudio.txt', "r+") as file:
        text = file.read()
        
text2speech("noAudio", text) 