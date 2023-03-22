import RPi.GPIO as GPIO

# import the library
from motor import *
    
GpioPins = [10, 25, 8, 7]
motor = Motor(GpioPins)

while True:
    motor.run()

# Declare an named instance of class pass a name and motor type
