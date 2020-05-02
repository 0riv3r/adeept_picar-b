#!/usr/bin/env/python
# File name     : App.py
# Author        : 0riv3r
# Desc          : Application faunctionality & control
#                 A central place for saving and serving the Rover global state
#                 A central place to manage functionality decisions

import BT
import LED
import move
import servo
import Vision
import time
import ultra
from enum import Enum


# ---------------------------------------------------------

# SPEED
MAX_SPEED = 100
MIN_SPEED = 60
SPPED_STEP = 10  # every speed change is a jump of 10
INIT_SPEED = 70

# ---------------------------------------------------------

# DISTANCE
RANGE_MIN = 0.2  # minimum distance from object

# ---------------------------------------------------------

# LED

# A LED thread
ledthread = LED.LED_ctrl()
ledthread.start()

# ---------------------------------------------------------

# Vision
# 0riv3r vision module that deals with GC vision

vision = Vision.Vision()

# Detect Items
VEHICLE_PROPERTIES = ['Vehicle', 'Wheel']

sleepWhenMove = 1
speed = 80
wheelsTurnAngle = 0.5


class TargetItems(Enum):
    VEHICLE = VEHICLE_PROPERTIES

# ---------------------------------------------------------


class App:

    speed = INIT_SPEED
    # Bluetooth
    btThread = BT.BT()
    btThread.start()

    def __init__(self):

        # A counter to be used when deciding on the camera movement direction
        self.cameraMoveCount = 0

        self.targetItem = TargetItems.VEHICLE

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

        if vision.isDetectItem(frame_image, self.targetItem.value):

            # *** The item is detected ***

            detect = True
            print(">  " + self.targetItem.value[0] + " Detected!  <")

            self.ItemDetectedSound(1)

            """
            get the last direction of the camera, 
            which is where the item is found
            details on the camera direction decison in the else block below
            """
            direction = (self.cameraMoveCount-1) % 3

            if direction == 0:
                servo.ahead()
                time.sleep(0.3)
                self.moveFw()

            elif direction == 1:
                servo.ahead()
                servo.lookleft(100)
                time.sleep(0.3)
                servo.turnLeft(wheelsTurnAngle)
                self.moveFw()

            elif direction == 2:
                servo.ahead()
                servo.lookright(100)
                time.sleep(0.3)
                servo.turnRight(wheelsTurnAngle)
                self.moveFw()

            time.sleep(sleepWhenMove)
            move.motorStop()
            self.ItemDetectedSound(0)

        else:  # *** The item is not detected ***

            move.motorStop()

            """
            Camera movement
            cameraMoveCount counter is increased at each time it gets here
            cameraMoveCount mod 3 - give us each time one value from the set: 0,1,2
            each such value represents a different direction for the camera
            """
            direction = self.cameraMoveCount % 3
            self.cameraMoveCount += 1

            if direction == 0:
                servo.ahead()

            elif direction == 1:
                servo.ahead()
                servo.lookleft(100)

            elif direction == 2:
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
        return self.targetItem.value[0]

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
