#!/usr/bin/env/python
# File name     : or_Movements.py
# Author        : 0riv3r
# Desc          : Rover movements required by App

import servo
import ultra
import move
import time


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
