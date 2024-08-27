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

#if motion detected -> call face_recognition -> if face_recognition() == type.String -> string data = face_recognition() + "motion detected"
        #face_recognition()
        #print name

face_recog_result = face_recognition()
if isinstance(face_recog_result, str):
        # If face_recognition returns a string, print it in JSON format
        result = {"motion detected": face_recog_result}
        save_activity(result)
    else:
        # If not a string, call voice_recognition
        voice_recognition()
    
attachment = MIMEText(json.dumps(data))
attachment.add_header('Content-Disposition', 'attachment', 
                      filename="activity_log_file.json")
msg.attach(attachment)
