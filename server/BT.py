#!/usr/bin/env/python
# File name     : BT.py
# Author        : 0riv3r
# Desc          : Bluetooth, Audio
#
# BT Setup instractions can be found at the bottom

import subprocess
import threading
from enum import Enum

# ---------------------------------------------------------

SPEAKER_MAC = '2C:41:A1:89:72:03'  # my speaker's MAC
AUDIO_PATH = '/home/pi/Audio/'


class Sounds(Enum):
    CARTOON_BANGS = 'cartoon-3bangs.wav'
    CARTOON_BOING = 'cartoon-boing.wav'
    CARTOON_HORN = 'cartoon-horn.wav'
    CARTOON_POLICE = 'cartoon-police.wav'
    CARTOON_THROW = 'cartoon-throw.wav'
    CARTOON_DROPS = 'cartoon-3drops.wav'
    CARTOON_BUMP = 'cartoon-bump.wav'
    CARTOON_LITTLE_BOING = 'cartoon-littleBoing.wav'
    CARTOON_RUNNING_FROG = 'cartoon-runningFrog.wav'
    CARTOON_TRAIN = 'cartoon-train.wav'

# ---------------------------------------------------------


class BT(threading.Thread):

    def playSound(self, soundsEnum):
        path = AUDIO_PATH + soundsEnum.value
        playCmd = 'aplay -D bluealsa:DEV=' + SPEAKER_MAC + ' ' + path
        subprocess.call([playCmd], shell=True)


"""
0riv3r

*********************************************************************
******************        Bluetooth Setup        ********************
*********************************************************************


Connect to a bluetooth speaker
==============================

http://denvycom.com/blog/playing-audio-over-bluetooth-on-rasbperry-pi-command-line/

https://www.digikey.com/en/maker/blogs/raspberry-pi-wi-fi-bluetooth-setup-how-to-configure-your-pi-4-model-b-3-model-b


install the following if needed
-------------------------------

Completely remove and purge all pulseaudio if installed!
$ sudo reboot now

https://www.sigmdel.ca/michel/ha/rpi/bluetooth_n_buster_01_en.html

$ sudo apt update && sudo apt upgrade -y
$ sudo reboot
$ sudo apt install bluealsa
$ sudo nano /lib/systemd/system/bluealsa.service
[Unit]
Description=BluezALSA proxy
Requires=bluetooth.service
After=bluetooth.service

[Service]
Type=simple
User=root
ExecStart=/usr/bin/bluealsa -p a2dp-source -p a2dp-sink

$ sudo adduser pi bluetooth
$ sudo nano /lib/systemd/system/bluetooth.service
[Unit]
Description=Bluetooth service
Documentation=man:bluetoothd(8)
ConditionPathIsDirectory=/sys/class/bluetooth

[Service]
Type=dbus
BusName=org.bluez
ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=sap
NotifyAccess=main
#WatchdogSec=10
#Restart=on-failure
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
LimitNPROC=1
ProtectHome=true
ProtectSystem=full

[Install]
WantedBy=bluetooth.target
Alias=dbus-org.bluez.service


$ sudo reboot

$ sudo systemctl status blue*
$ q
$ sudo systemctl restart bluetooth.service
$ sudo systemctl status bluetooth.service


connect to a blutooth speaker/device
------------------------------------

https://www.digikey.com/en/maker/blogs/raspberry-pi-wi-fi-bluetooth-setup-how-to-configure-your-pi-4-model-b-3-model-b

$ bluetoothctl
[bluetooth]# power on
[bluetooth]# agent on

* set the speaker on discovery mode

[bluetooth]# scan on
Discovery started
[CHG] Controller DC:A6:32:90:87:2D Discovering: yes
[NEW] Device C0:28:8D:82:12:AC C0-28-8D-82-12-AC
[NEW] Device 2C:41:A1:89:72:03 LE-bruce

[bluetooth]# pair 2C:41:A1:89:72:03
Attempting to pair with 2C:41:A1:89:72:03
[CHG] Device 2C:41:A1:89:72:03 Connected: yes
[CHG] Device 2C:41:A1:89:72:03 Name: bruce
[CHG] Device 2C:41:A1:89:72:03 Paired: yes
Pairing successful

[bluetooth]# trust 2C:41:A1:89:72:03
[CHG] Device 2C:41:A1:89:72:03 Trusted: yes
Changing 2C:41:A1:89:72:03 trust succeeded

[bluetooth]# connect 2C:41:A1:89:72:03
Attempting to connect to 2C:41:A1:89:72:03
[CHG] Device 2C:41:A1:89:72:03 Connected: yes
[CHG] Device 2C:41:A1:89:72:03 Name: bruce
[CHG] Device 2C:41:A1:89:72:03 Alias: bruce
Connection successful

[bruce]# disconnect 2C:41:A1:89:72:03
Attempting to disconnect from 2C:41:A1:89:72:03
[CHG] Device 2C:41:A1:89:72:03 ServicesResolved: no
Successful disconnected
[CHG] Device 2C:41:A1:89:72:03 Connected: no

[bluetooth]# quit


Play Audio
==========

https://www.sigmdel.ca/michel/ha/rpi/bluetooth_01_en.html

aplay -D bluealsa:DEV=2C:41:A1:89:72:03 /usr/share/sounds/alsa/Front_Center.wav


============================================================================================================
"""
