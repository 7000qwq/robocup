import base64
import cv2
import datetime
import math
import operator
import os
import requests
from PIL import Image


class Robocup():
    origin_pics = []
    item_labelled_pics = []
    face_item_labelled_pics = []

    def __init__(self):
        self.get_token()
        self.register_face()

    def register_face(self):
        return "Register"

    def read_pics(self):
        return "Read"

    def detect_items(self):
        return "Detection"

    def detect_faces(self):
        os.system("python detect.py")
        return "Detection"

    def label_faces(self):
        return "Labelled"

    def save_results(self):
        return self._detection




if __name__ == "__main__":
    robocup = Robocup()
    robocup.face_registration()
    robocup.read_pics()
    robocup.detect_items()
    robocup.detect_faces()
    robocup.label_faces()
    robocup.save_results()
