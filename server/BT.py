# Bluetooth
# Audio

import subprocess


class BT:

    def __init__(self):
        self.audioFilesDir = '/home/pi/Audio/'

    def playAudio(self, filePath):
        path = self.audioFilesDir + filePath
        # my speaker's MAC: '2C:41:A1:89:72:03'
        subprocess.call(['aplay -D bluealsa:DEV=2C:41:A1:89:72:03 ' + path], shell=True)         