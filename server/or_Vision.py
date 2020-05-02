#!/usr/bin/env/python
# File name     : or_Vision.py
# Author        : 0riv3r
# Desc          : Vision functionality management required by App
#                 Use Google Cloud Vision API

"""
    Google Vision API and Raspberry Pi Camera for labaling pictures.
    Based on the tutorial at:
    https://cloud.google.com/vision/docs/how-to

    Use Google Cloud Vision on the Raspberry Pi
    to take a picture with the Raspberry Pi Camera and classify it with the
    Google Cloud Vision API.

    1. The camera takes a picture of an object
    2. upload the picture taken to Google Cloud
    3. GC-Vision analyze the picture and return labels as a json response

    This script uses the Vision API's label detection capabilities to find
    a label based on an image's content.
"""

from google.cloud import vision as gcVision
from PIL import Image
import os

# ---------------------------------------------------------

# GCP

KEY_FILE = "/home/pi/keys/pivision1-c7e6e5c23f0d.json"
GC_ENV_VAR = "GOOGLE_APPLICATION_CREDENTIALS"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    "/home/pi/keys/pivision1-c7e6e5c23f0d.json"

# ------------------------------------


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class Vision:

    def __init__(self):
        self.client = gcVision.ImageAnnotatorClient()
        self.pt1 = 0.0
        self.pt2 = 0.0

    def isDetectItem(self, frame_image, lstTargetProperties):
        detect = False
        img = Image.fromarray(frame_image)
        img.save("image.jpg")
        with open('image.jpg', 'rb') as image_file:
            content = image_file.read()
        image = gcVision.types.Image(content=content)

        # response = self.client.logo_detection(image=image)
        # response = self.client.label_detection(image=image)
        # labels = response.label_annotations
        # for labely in labels:
        # 	print(labely.description)
        # if any(label.description in lstTargetProperties for label in labels):
        #     detect = True

        objects = self.client.object_localization(image=image) \
            .localized_object_annotations

        for obj in objects:
            print("Item identified: " + obj.name)
            # if obj.name == "Wheel":
            # if obj.name in lstTargetProperties:
            vertices = obj.bounding_poly.normalized_vertices
            self.pt1 = Point(vertices[0].x, vertices[0].y)
            self.pt2 = Point(vertices[2].x, vertices[2].y)

        return detect

    def getBoundingPolygonPt1(self):
        return self.pt1

    def getBoundingPolygonPt2(self):
        return self.pt2
