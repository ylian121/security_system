# library imports
import cv2
import os
import numpy as np

# simple rec face support
import face_recognition
import glob


# for time for facial
from datetime import date, datetime, timedelta
from time import sleep

# for sending the activity log email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

# Function to send an email with a JSON file attached

# File paths
activity_info_file = 'activity_log_file.json'

# Function to load activity data from JSON file
def load_activity():
    if os.path.exists(activity_info_file):
        with open(activity_info_file, 'r') as file:
            return json.load(file)
    return {}

# Function to save activity data to JSON file
def save_activity(data):
    with open(activity_info_file, 'w') as file:
        json.dump(data, file, indent=4)

# Load the activity data
activity_data = load_activity()

# simple face rec class
class SimpleFacerec:

    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:

            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:

            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:

                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing

        return face_locations.astype(int), face_names



# turn on camera
def turn_on_camera():

    # Load Camera
    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow("Camera Feed", frame)

        k = cv2.waitKey(30) & 0xff

        if k == 27:
            break

    cap.release()

    cv2.destroyAllWindows()



# face recognition + print for activity log
def face_recognition(folder="faces"):
    # Encode faces from the specified folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images(folder)

    # Load Camera
    cap = cv2.VideoCapture(0)

    recognized_name = None

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=20)

    while datetime.now() < end_time:

        print(datetime.now())
        sleep(1)
        
        ret, frame = cap.read()

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)

        for name in face_names:

            if name != "Unknown":

                recognized_name = name
                print(f"Recognized: {recognized_name}")
                
                return recognized_name

        for face_loc, name in zip(face_locations, face_names):

            #print(f"Recognized: {name}")

            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        cv2.imshow("Frame", frame)

        k = cv2.waitKey(30) & 0xff

        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return False



# delete user
def delete_user(name, folder="faces"):
    #name = input("Enter the name of the user to delete: ")
    filepath = os.path.join(folder, f"{name}.jpg")
    
    if os.path.exists(filepath):

        os.remove(filepath)

        print(f"{name}'s face image has been deleted.")
    else:
        print(f"No face image found for {name}.")



# face recognition without print for log
def facial_recognition(folder="faces"):
    # Encode faces from the updated folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images(folder)

    # Load Camera
    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)

        for face_loc, name in zip(face_locations, face_names):

            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        cv2.imshow("Frame", frame)

        k = cv2.waitKey(30) & 0xff

        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def detect_people(video_source=0, window_size=(640, 480), win_stride=(8, 8)):
    # HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Load Camera or Video
    cap = cv2.VideoCapture(video_source)

    while True:

        ret, frame = cap.read()

        # resizing
        frame = cv2.resize(frame, window_size)

        # using a greyscale picture
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        boxes, weights = hog.detectMultiScale(frame, winStride=win_stride)

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        for (xA, yA, xB, yB) in boxes:

            # display the detected people
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

            #print("Detecting people...")

            face_recog_result = face_recognition()
            if isinstance(face_recog_result, str):
                # If face_recognition returns a string, save it in JSON format
                result = {"person detected": face_recog_result}
                save_activity(result)
                return    
            
            return False

        cv2.imshow("Frame", frame)

        k = cv2.waitKey(30) & 0xff

        if k == 27:
            break

    # Release the capture and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


def capture_new_user(name, folder="faces"):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return

    # Allow some time for the camera to adjust
    time.sleep(2)  # Optional: Let the camera warm up

    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture image")
        return
    
    cv2.imshow("Capture Face", frame)
    print("Taking picture in 5 seconds...")
    
    time.sleep(5)  # Delay before taking the picture

    # Capture the photo
    filepath = os.path.join(folder, f"{name}.jpg")
    cv2.imwrite(filepath, frame)
    
    print(f"Photo saved as {filepath}")

    # Release the camera and close any open windows
    cap.release()
    cv2.destroyAllWindows()




