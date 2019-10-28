"""
    OutletController
    - controls the motor than rotates according to specified outlet
    - calculates angle to be rotated
"""

import RPi.GPIO as IO
import time

class OutletController:
    def __init__(self, pin, freq=50):
        """
            may be centralize GPIO settings in another file later
        """
        IO.setmode(IO.BOARD)
        IO.setup(pin, IO.OUT)
        self.pin = pin          # GPIO pin
        self.freq = freq        # PWM signal frequency, refer to data sheet of your motor
        self.rest_time = 0.5    # seconds
        # set up PWM signal to control servo motor
        self.p = IO.PWN(self.pin, self.freq)
        # set to natural position
        p.start(0)
        # pass

    def __main__(self):
        pass

    """
        __reset__
        move to natural position
            :arg    @None
            :return @None
    """
    def __reset__(self):
        p.changeDutyCycle(0)
        time.sleep(0.5)

    """
        __move_to__
        move to certain position according to outlet id
            :arg    @String outlet
            :return @None
    """
    def __move_to__(self, outlet):
        # convert id to angle for rotation
        pass
