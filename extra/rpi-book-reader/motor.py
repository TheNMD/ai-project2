"""Module defining Motor class and related functions.

Uses Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
"""

from enum import Enum
from RpiMotorLib.RpiMotorLib import BYJMotor

class Motor:
    """Represents a 28BYJ-48 unipolar stepper motor driven by a ULN2003 stepper motor driver.

    Attributes:
        GPIO_PINS: An array of 4 GPIO pins connected to IN1-IN4 on the stepper motor driver.
    """
    STEPS_PER_REVOLUTION = 64  # The amount of steps that the motor needs to take to turn 1 revolution

    class SteppingMode(Enum):
        """Valid motor stepping modes."""
        FULL = "full",
        HALF = "half",
        WAVE = "wave"

    def __init__(self, GPIO_PINS):
        """Initializes Motor object using RPiMotorLib library."""
        self.MOTOR = BYJMotor()
        self.GPIO_PINS = GPIO_PINS
        self.stepping_mode = Motor.SteppingMode.FULL

    @property
    def stepping_mode(self):
        return self.stepping_mode

    @stepping_mode.setter
    def stepping_mode(self, value):
        try:
            self.stepping_mode = Motor.SteppingMode(value)
        except ValueError:
            raise Exception("Stepping mode not valid.")

    def move(self, degrees):
        """Rotates the motor a specified number of degrees, clockwise or counterclockwise.

        Args:
            degrees: A positive or negative integer indicating the number of
                degrees to move the motor
        """
        steps = Motor.__convert_to_steps(degrees)

        """Change motor direction if degrees is negative """
        if (degrees < 0):
            ccwise = True
        else:
            ccwise = False

        self.MOTOR.motor_run(self.GPIO_PINS, wait=0, steps=steps, ccwise=ccwise,
                  verbose=False, steptype=self.stepping_mode, initdelay=0)

    @staticmethod
    def __convert_to_steps(self, degrees):
        """Converts degrees to motor steps.

        Args:
            degrees: The number of degrees to convert to motor steps.

        Returns:
            A rounded integer indicating the number of motor steps equivalent
            to the number of degrees specified by the user.
        """
        steps = Motor.STEPS_PER_REVOLUTION * 1/360 * degrees    # [steps/rev] * (1rev / 360deg) * [deg]
        return steps
