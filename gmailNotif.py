from new_user import capture_new_user, facial_recognition
from delete_user import delete_user
from faceRec import face_recognition
from peopleDetectionFunction import detect_people

import cv2
import os
from simple_facerec import SimpleFacerec


# link to the notification page
#https://raw.githubusercontent.com/PajakaL/CS179J-Pajaka-Parnika-Yongyan-Briana/master/notification.json?token=GHSAT0AAAAAACQQCKKWXPD2LZUCGW2NHSSEZWNHMLQ


def send_email():
    while True:

    # if motion is detected:
        #print to json file
