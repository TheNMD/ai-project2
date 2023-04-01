from PIL import Image
from pytesseract import pytesseract

from gtts import gTTS

from playsound import playsound

def image2text(imagePath):
    # Path to tesseract.exe
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Opening the image & storing it in an image object
    img = Image.open(imagePath)

    # Passing the image object to image_to_string() function extract the text from the image
    text = pytesseract.image_to_string(img)

    # Saving the extracted text
    with open("./texts/sample.txt", "w+") as file:
        file.write(text)

def text2speech(textPath):
    # The text that you want to convert to audio
    with open(textPath, "r+") as file:
        text = file.read()
    
    # Passing the text and language to the engine, 
    # slow=False means the audio will have normal speed
    audio = gTTS(text=text, lang='en', slow=False)
    
    # Saving the converted audio in a mp3 format
    audio.save("./audio/sample.mp3")

def playaudio(audioPath):
    playsound(audioPath)

# image2text('./images/sample.jpg')
# text2speech('./texts/sample.txt')
playaudio('./audio/sample.mp3')