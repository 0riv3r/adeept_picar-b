"""
Google Vision API and Raspberry Pi Camera for labaling pictures.
Based on the tutorial at:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Use Google Cloud Vision on the Raspberry Pi 
to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   

1. The camera takes a picture of an object
2. upload the picture taken to Google Cloud 
3. GC-Vision analyze the picture and return labels as a json response

This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

"""

import picamera

from google.cloud import vision
client = vision.ImageAnnotatorClient()


def takephoto():
    camera = picamera.PiCamera()
    camera.capture('image.jpg')

def getPictureLabels():
    takephoto() # First take a picture
    """Run a label request on a single image"""

    with open('image.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # response = client.logo_detection(image=image)
    response = client.label_detection(image=image)
    return(response.label_annotations)

def isTargetObject(target):
    labels = getPictureLabels()
    print(labels)

    # for label in labels:
    #     print(label.description)

    if any(label.description == target for label in labels):
        print("YESSSSSSSSSSSSSSSSSS!")


if __name__ == '__main__':
    isTargetObject("car")

# ---------------------------
####  EXECUTE THIS FILE  ####
# ---------------------------
# export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/keys/pivision1-c7e6e5c23f0d.json"
# pwd
#   /home/pi/adeept_picar-b/server/
# python3 camera_vision_label.py

########################################################################################

# ----------------
####  SETUP   ####
# ----------------
# $ sudo pip3 install --upgrade pip
# $ sudo apt-get install libjpeg8-dev
# $ sudo pip3 install --upgrade google-api-python-client
# $ sudo pip3 install --upgrade Pillow
# $ sudo apt-get install python-picamera

# $ pip install google-cloud-vision
# $ pip install --upgrade google-cloud-storage
# $ export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/keys/pivision1-c7e6e5c23f0d.json"

########################################################################################

# -------------------
####  RESPONSE   ####
# -------------------

# [
# mid: "/m/03b6_4" description: "Steering wheel" score: 0.83581871 topicality: 0.83581871 ,  
# mid: "/m/083wq" description: "Wheel" score: 0.82492822 topicality: 0.82492822 , 
# mid: "/m/0h8lskq" description: "Steering part" score: 0.82124043 topicality: 0.82124043 ,
# mid: "/m/07yv9" description: "Vehicle" score: 0.78287292 topicality: 0.78287292 , 
# mid: "/m/08dz3q" description: "Auto part" score: 0.77648753 topicality: 0.77648753 , 
# mid: "/m/0k4j" description: "Car" score: 0.74546075 topicality: 0.74546075 , 
# mid: "/m/02mrp" description: "Electronics" score: 0.7308113 topicality: 0.7308113 , 
# mid: "/m/047vmg8" description: "Rim" score: 0.70876068 topicality: 0.70876068 , 
# mid: "/m/0h8ly30" description: "Automotive wheel system" score: 0.69629019 topicality: 0.69629019 , 
# mid: "/m/02mnkq" description: "Bumper" score: 0.68434745 topicality: 0.68434745
# ]

