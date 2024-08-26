import cv2
import os
from simple_facerec import SimpleFacerec

def delete_user(folder="faces"):
    name = input("Enter the name of the user to delete: ")
    filepath = os.path.join(folder, f"{name}.jpg")
    
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"{name}'s face image has been deleted.")
    else:
        print(f"No face image found for {name}.")

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
