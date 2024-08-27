import cv2
from simple_facerec import SimpleFacerec

from datetime import date, datetime, timedelta
from time import sleep


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

