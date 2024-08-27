import cv2
import os
from simple_facerec import SimpleFacerec

def capture_new_user(name, folder="faces"):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    print("Press 'c' to capture a photo, or 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        cv2.imshow("Capture Face", frame)
        
        k = cv2.waitKey(1) & 0xff
        if k == ord('c'):
            # Capture the photo
            filepath = os.path.join(folder, f"{name}.jpg")
            cv2.imwrite(filepath, frame)
            print(f"Photo saved as {filepath}")
            break
        elif k == ord('q'):
            print("Quitting without saving.")
            break
    
    cap.release()
    cv2.destroyAllWindows()

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
