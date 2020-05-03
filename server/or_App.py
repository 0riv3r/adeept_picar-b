#!/usr/bin/env/python
# File name     : or_App.py
# Author        : 0riv3r
# Desc          : Application faunctionality & control
#                 A central place for saving and serving the Rover global state
#                 A central place to manage functionality decisions

import or_BT as BT
import LED
import or_Movements
import or_Vision as Vision
from enum import Enum


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
VEHICLE_PROPERTIES = ['Vehicle', 'Wheel', 'Toy vehicle', 'Tire', 'car']


class TargetItems(Enum):
    VEHICLE = VEHICLE_PROPERTIES

# ---------------------------------------------------------


class App:

    # Bluetooth
    btThread = BT.BT()
    btThread.start()

    def __init__(self):

        self.bodyMovements = or_Movements.MoveBody()
        self.headMovements = or_Movements.MoveHead()

        # A counter to be used when deciding on the camera movement direction
        self.cameraMoveCount = 0

        self.targetItem = TargetItems.VEHICLE

    # ***************************    Mobile App   **************************

    def btn_A(self):
        self.police()

    def btn_B(self):
        self.rainbow()

    # **********************    Vision - Detect Item   **********************

    def detectItem(self, frame_image):

        sleepBeforeDrive = 0.3
        sleepDistance = 0.5
        stabilizingSleep = 1
        wheelsTurnAngle = 0.5
        headAngle = 100

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
            self.bodyMovements.moveBodyDirection(direction, sleepBeforeDrive,
                                                 sleepDistance, headAngle,
                                                 wheelsTurnAngle)
            self.ItemDetectedSound(0)

        else:  # *** The item is not detected ***

            """
            TODO:
            follow a moving item with the head
            decide if to follow the item by driving or only by head movements
            follow a with the camera(head):
            according to the placement of the objct dots
            move the head-camera in order to keep the detected item in the middle
            """

            """
            Camera movement
            cameraMoveCount counter is increased at each time it gets here
            cameraMoveCount mod 3 - give us each time one value from the set: 0,1,2
            each such value represents a different direction for the camera
            """
            direction = self.cameraMoveCount % 3
            self.cameraMoveCount += 1
            self.headMovements.moveHeadDirection(direction, stabilizingSleep,
                                                 headAngle)

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

    def getBoundingPolygonPt1(self):
        return vision.getBoundingPolygonPt1()

    def getBoundingPolygonPt2(self):
        return vision.getBoundingPolygonPt2()

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
