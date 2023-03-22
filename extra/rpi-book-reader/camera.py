"""Module defining code to setup the camera.

Uses Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
"""

import datetime

from picamera import PiCamera
from datetime import datetime

class Camera:
    """Represents a camera connected to the Raspberry Pi's camera port.

    Attributes:
        camera: The camera connected to the Raspberry Pi
    """

    def __init__(self):
        """Initializes Camera object using PiCamera library."""
        self.camera = PiCamera()

    def take_picture(self):
        """Snaps a single picture, gives it a timestamp, and stores the file in
        a user-specified directory."""
        self.camera.capture("./images/" + self.__get_timestamp() + ".jpg")

    def start_video(self):
        self.camera.start_recording("./videos/" + self.__get_timestamp() + "")

    def stop_video(self):
        self.camera.stop_recording();

    def __get_timestamp(self):
        """Gets the current time in ISO format."""
        return datetime.now().isoformat()
