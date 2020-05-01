#!/usr/bin/env/python
# File name     : App.py
# Author        : 0riv3r
# Desc          : Application faunctionality & control
#                 A central place for saving and serving the Rover global state
#                 A central place to manage functionality decisions


# SPEED
# -----
MAX_SPEED = 100
MIN_SPEED = 60
SPPED_STEP = 10
INIT_SPEED = 70


class App:

    def __init__(self):
        self.speed = INIT_SPEED

    # input: string
    # Change the speed value according to the given string value
    def speedControl(self, gas='ignore'):
        try:
            if (gas == 'add' and self.speed < MAX_SPEED):
                self.speed += SPPED_STEP
            elif (gas == 'reduce' and self.speed > MIN_SPEED):
                self.speed -= SPPED_STEP
            return self.speed
        except TypeError:
            pass

    # input: int
    # Set the speed value to the given int value
    def setSpeed(self, iSpeed):
        try:
            self.speed = iSpeed
        except TypeError:
            pass
