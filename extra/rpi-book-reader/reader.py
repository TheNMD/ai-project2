"""Module containing text-to-speech code.

Uses Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
"""

from gtts import gTTS
from enum import Enum
from kivy.core.audio import SoundLoader, Sound
from pathlib import Path
from PIL import Image
from playsound import *
from pydub import AudioSegment
from pydub.playback import play
from pytesseract import *

class Reader:
    """Reads aloud text from camera according to the user's preferences.

    Attributes:
        voice: The voice engine used to speak words aloud.
        paused: Whether or not the reader is paused.
    """

    class Voice(Enum):
        """Valid voice options."""
        GOOGLE = 1,
        PYTTSX = 2

    def __init__(self, PATH_TO_TESSERACT_EXE=None, voice=None):
        """Initializes Reader class"""
        if voice is None:
            self.voice = Reader.Voice.GOOGLE
        else:
            self.voice = voice

        self.paused = True

        if PATH_TO_TESSERACT_EXE is not None:
            pytesseract.tesseract_cmd = PATH_TO_TESSERACT_EXE

    def change_voice(self, voice):
        """Changes the reader's voice to the specified voice"""
        try:
            self.voice = voice;
        except ValueError:
            raise Exception(voice + "is not a valid voice type." )

    def pause(self):
        """Pauses the reader"""
        self.paused = True

    def play(self):
        """Plays the reader."""
        self.__read("hello")
        self.paused = False

    def read_image(self, image_file):
        string = self.__image_to_string(image_file)
        self.__read(string)

    def __image_to_string(self, image_file):
        return pytesseract.image_to_string(Image.open(image_file))

    def __read(self, string):
        if (self.voice == Reader.Voice.GOOGLE):
            tts = gTTS(text=string, lang='en')
            audio_file_path = str(Path(__file__).parent / "audio/temp.mp3")

            if Path(audio_file_path).is_file():
                Path(audio_file_path).unlink()
            tts.save(audio_file_path)

            print(audio_file_path)
            sound = AudioSegment.from_file(audio_file_path, format="mp3")
            play(sound)
