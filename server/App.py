#!/usr/bin/env/python
# File name     : App.py
# Author        : 0riv3r
# Desc          : Application faunctionality & control
#                 A central place for saving and serving the Rover global state
#                 A central place to manage functionality decisions

import subprocess
import threading
import BT
import LED
import move
import servo
import Vision
import io
from PIL import Image
import os
import subprocess
import time
import ultra


# ---------------------------------------------------------

# SPEED
MAX_SPEED = 100
MIN_SPEED = 60
SPPED_STEP = 10
INIT_SPEED = 70

# ---------------------------------------------------------

# DISTANCE
RANGE_MIN = 0.2

# ---------------------------------------------------------

# LED
ledthread = LED.LED_ctrl()
ledthread.start()

# ---------------------------------------------------------

# Vision
vision = Vision.Vision()

# Detect Items
VEHICLE_PROPERTIES = ['Vehicle', 'Wheel']

TARGET = VEHICLE_PROPERTIES

sleepWhenMove = 1
speed = 80
wheelsTurnAngle = 0.5

# ---------------------------------------------------------

class App:

    speed = INIT_SPEED
    # Bluetooth
    btThread = BT.BT()
    btThread.start()

    def __init__(self):
        self.cameraMoveCount = 0

    # ****************************    Speed   *****************************

    # input: string
    # Change the speed value according to the given string value
    # if gas value is not given, it will only return the current speed value
    def speedControl(self, gas='ignore'):
        try:
            if (gas == 'add' and App.speed < MAX_SPEED):
                App.speed += SPPED_STEP
            elif (gas == 'reduce' and App.speed > MIN_SPEED):
                App.speed -= SPPED_STEP
            return App.speed
        except TypeError:
            pass

    # input: int
    # Set the speed value to the given int value
    def setSpeed(self, iSpeed):
        try:
            App.speed = iSpeed
        except TypeError:
            pass

    # ***************************    Mobile App   **************************

    def btn_A(self):
        self.police()

    def btn_B(self):
        self.rainbow()
            
    # **********************    Vision - Detect Item   **********************

    def detectItem(self, frame_image):
        detect = False
        if vision.isDetectItem(frame_image, TARGET):
            detect = True
            print(">  " + TARGET[0] + " Detected!  <")
            
            self.ItemDetectedSound(1)
            side = (self.cameraMoveCount-1)%3

            if side == 0:
                servo.ahead()
                time.sleep(0.3)
                self.moveFw()

            elif side == 1:
                servo.ahead()
                servo.lookleft(100)
                time.sleep(0.3)
                servo.turnLeft(wheelsTurnAngle)
                self.moveFw()

            elif side == 2:
                servo.ahead()
                servo.lookright(100)
                time.sleep(0.3)
                servo.turnRight(wheelsTurnAngle)
                self.moveFw()

            time.sleep(sleepWhenMove)
            move.motorStop()
            self.ItemDetectedSound(0)

        else:
            
            move.motorStop()

            side = self.cameraMoveCount%3
            self.cameraMoveCount += 1
            if side == 0:
                servo.ahead()

            elif side == 1:
                servo.ahead()
                servo.lookleft(100)

            elif side == 2:
                servo.ahead()
                servo.lookright(100)
                
            time.sleep(sleepWhenMove)
            move.motorStop()

        return detect


    def ItemDetectedSound(self, invar):
        if invar:
            LED.ledfunc = 'police'
            ledthread.resume()
            App.btThread.playSound(BT.Sounds.CARTOON_THROW)
        else:
            LED.ledfunc = ''
            ledthread.pause()

    def getTragetItem(self):
        return TARGET[0]

    def moveFw(self):
        if(ultra.checkdist() > RANGE_MIN):
            print("ultra.checkdist(): " + str(ultra.checkdist()))
            move.move(App.speed, 'forward')

# **********************    Functions   **********************

    def police(self):
        if LED.ledfunc != 'police':
            LED.ledfunc = 'police'
            ledthread.resume()
            App.btThread.playSound(BT.Sounds.CARTOON_POLICE)
        elif LED.ledfunc == 'police':
            LED.ledfunc = ''
            ledthread.pause()

    def rainbow(self):
        if LED.ledfunc != 'rainbow':
            LED.ledfunc = 'rainbow'
            ledthread.resume()
            App.btThread.playSound(BT.Sounds.CARTOON_RUNNING_FROG)
        elif LED.ledfunc == 'rainbow':
            LED.ledfunc = ''
            ledthread.pause()