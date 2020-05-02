#!/usr/bin/env/python
# File name     : vision_labeled.py
# Author        : 0riv3r
# Desc          : Use this file to get lists of items' properties from GC Vision

"""
Google Vision API and Raspberry Pi Camera for labaling pictures.
Based on the tutorials at:
https://cloud.google.com/vision/docs/how-to
Use Google Cloud Vision on the Raspberry Pi
to take a picture with the Raspberry Pi Camera and classify it with the 
Google Cloud Vision API.
1. The camera takes a picture of an object
2. upload the picture taken to Google Cloud
3. GC-Vision analyze the picture and return labels as a json response
This script uses the Vision API's label detection capabilities to find a label
based on an image's content.
"""

import picamera 

from google.cloud import vision
client = vision.ImageAnnotatorClient()

# Execute:
# $ PS1='\u:\W\$ '    # to reduce the length of the cli prompt
# $ export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/keys/pivision1-c7e6e5c23f0d.json"
# $ python3 gcVision.py


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y


def main():
    # First take a picture
    camera = picamera.PiCamera()
    camera.capture('image.jpg')

    """Run a label request on a single image"""

    with open('image.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # response = client.logo_detection(image=image)
    # response = client.label_detection(image=image)
    # print("response: " + str(response))
    # labels = response.label_annotations
    # for label in labels:
    #     print(label.description)

    objects = client.object_localization(
        image=image).localized_object_annotations

    # print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        # print('\n{} (confidence: {})'.format(object_.name, object_.score))
        # if object_.name in ["Vehicle", "Car", "Wheel", "Tire"]:
        print(str(object_))
        # print('Normalized bounding polygon vertices: ')
        # for vertex in object_.bounding_poly.normalized_vertices:
        #     print(' - ({}, {})'.format(vertex.x, vertex.y))
        vertices = object_.bounding_poly.normalized_vertices
        pt1 = Point(vertices[0].x, vertices[0].y)
        pt2 = Point(vertices[2].x, vertices[2].y)
        print(str(pt1.getX()) + "," + str(pt1.getY()))
        print(str(pt2.getX()) + "," + str(pt2.getY()))


if __name__ == '__main__':
    main()

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
