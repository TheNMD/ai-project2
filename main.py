from PIL import Image
from pytesseract import pytesseract
from playsound import playsound

import pyttsx3

def image2text(imageName):
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
    playsound('./audio/' + audioName + '.wav')

name = "sample1" # capture()
image2text(name)
text2speech(name, play=False)
playaudio(name)