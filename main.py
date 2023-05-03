from PIL import Image
from pytesseract import pytesseract
from playsound import playsound
from threading import Thread
import time

import pyttsx3

def image2text(imageName):
    # TODO How tesseract works, how to train tesseract on custom training data
    
    # Path to tesseract.exe
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

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

    # Saving the converted audio in a wav format
    engine.save_to_file(text, './audio/' + textName + '.wav')

    # Playing the audio
    if play:
        playaudio(textName)

    engine.runAndWait()

def playaudio(audioName):
    # TODO Stop, replay, slowdown, jump ahead features
    playsound('./audio/' + audioName + '.wav', block = False)
    input("Press Enter to continue")


class SoundPlayer:
    def __init__(self, sound_file):
        self.sound_file = './audio/' + sound_file + '.wav'
        self.paused = False
        self.thread = Thread(target=self._play_sound)

    def play(self):
        self.thread.start()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def _play_sound(self):
        playsound(self.sound_file, block=False)
        while True:
            if self.paused:
                time.sleep(0.1)
            else:
                playsound(self.sound_file, block=False)

def play_sound_with_pause(sound_file):
    player = SoundPlayer(sound_file)
    player.play()
    while True:
        input_text = input("Press Enter to pause/resume playback, or 'q' to quit... ")
        if input_text == "q":
            player.pause()
            break
        elif player.paused:
            player.resume()
        else:
            player.pause()

name = "sample2" # capture()
# image2text(name)
# text2speech(name, play=False)
# playaudio(name)
play_sound_with_pause(name)