#!/usr/bin/env/python
# File name     : or_Movements.py
# Author        : 0riv3r
# Desc          : Rover movements required by App

import servo
import ultra
import move
import time
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


class Direction(Enum):
    AHEAD = 0
    LEFT = 1
    RIGHT = 2


class MoveBody:

    speed = INIT_SPEED

    # ****************************    Speed   *****************************

    # input: string
    # Change the speed value according to the given string value
    # if gas value is not given, it will only return the current speed value
    def speedControl(self, gas='ignore'):
        try:
            if (gas == 'add' and MoveBody.speed < MAX_SPEED):
                MoveBody.speed += SPPED_STEP
            elif (gas == 'reduce' and MoveBody.speed > MIN_SPEED):
                MoveBody.speed -= SPPED_STEP
            return MoveBody.speed
        except TypeError:
            pass

    # input: int
    # Set the speed value to the given int value
    def setSpeed(self, iSpeed):
        try:
            MoveBody.speed = iSpeed
        except TypeError:
            pass

    def _secureMove(self, sleepDistance):
        if(ultra.checkdist() > RANGE_MIN):
            # print("ultra.checkdist(): " + str(ultra.checkdist()))
            move.move(MoveBody.speed, 'forward')
            time.sleep(sleepDistance)
            move.motorStop()

    def forward(self, sleepBeforeDrive, sleepDistance):
        servo.ahead()
        time.sleep(sleepBeforeDrive)
        self._secureMove(sleepDistance)

    def left(self, sleepBeforeDrive, headAngle, wheelsTurnAngle, 
             sleepDistance):
        servo.ahead()
        servo.lookleft(headAngle)
        time.sleep(sleepBeforeDrive)
        servo.turnLeft(wheelsTurnAngle)
        self._secureMove(sleepDistance)

    def right(self, sleepBeforeDrive, headAngle,
              wheelsTurnAngle, sleepDistance):
        servo.ahead()
        servo.lookright(headAngle)
        time.sleep(sleepBeforeDrive)
        servo.turnRight(wheelsTurnAngle)
        self._secureMove(sleepDistance)

    def moveBodyDirection(self, direction, sleepBeforeDrive,
                          sleepDistance, headAngle, wheelsTurnAngle):
        if direction == Direction.AHEAD:
            self.forward(sleepBeforeDrive, sleepDistance)

        elif direction == Direction.LEFT:
            self.left(sleepBeforeDrive, headAngle,
                      wheelsTurnAngle, sleepDistance)

        elif direction == Direction.RIGHT:
            self.right(sleepBeforeDrive, headAngle,
                       wheelsTurnAngle, sleepDistance)


class MoveHead:

    def ahead(self, sleepTime):
        servo.ahead()
        time.sleep(sleepTime)

    def left(self, sleepTime, headAngle):
        servo.ahead()
        servo.lookleft(headAngle)
        time.sleep(sleepTime)

    def right(self, sleepTime, headAngle):
        servo.ahead()
        servo.lookright(headAngle)
        time.sleep(sleepTime)

    def moveHeadDirection(self, direction, stabilizingSleep,
                          headAngle):
        if direction == Direction.AHEAD:
            self.ahead(stabilizingSleep)

        elif direction == Direction.LEFT:
            self.left(stabilizingSleep, headAngle)

        elif direction == Direction.RIGHT:
            self.right(stabilizingSleep, headAngle)
