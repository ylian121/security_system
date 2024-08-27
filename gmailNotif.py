from new_user import capture_new_user, facial_recognition
from delete_user import delete_user
from faceRec import face_recognition
from peopleDetectionFunction import detect_people

import cv2
import os
from simple_facerec import SimpleFacerec

activity_log_file = 'activity_log_file.json'

def load_activity():
    if os.path.exists(activity_info_file):
    with open(user_info_file, 'r') as file:
      return json.load(file)
  return {}

def save_activity(data):
  with open(user_info_file, 'w') as file:
    json.dump(data, file, indent = 4)

activity_data = load_activity()

while True:

    # if motion is detected:
        facial_recognition()
        #print name
    
    attachment = MIMEText(json.dumps(data))
    attachment.add_header('Content-Disposition', 'attachment', 
                          filename="foo.name.json")
    msg.attach(attachment)
