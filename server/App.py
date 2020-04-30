#!/usr/bin/env/python
# File name     : App.py
# Author        : 0riv3r
# Desc          : Application faunctionality & control


import appserver
import FPV


class App:

    def __init__(self):
        self.speed = 70
        self.speedControl(self.speed)

    def speedControl(self, gas):
        if (gas == 'add' and self.speed < 100):
            self.speed += 10
        elif (gas == 'reduce' and self.speed > 0):
            self.speed -= 10
        if gas:
            appserver.speed_set = self.speed
            FPV.speed_set = self.speed
        return self.speed
