from new_user import capture_new_user, facial_recognition
from delete_user import delete_user
from faceRec import face_recognition
from peopleDetectionFunction import detect_people

import cv2
import os
from simple_facerec import SimpleFacerec

while True:

    # if motion is detected:
        facial_recognition()
        #print name