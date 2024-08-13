import os
import cv2
import face_recognition as fr
import numpy as np


def get_encoded_faces():
    encoded = {}
    
    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".jpeg"):
                face = fr.load_image_file("faces/" + f)
                encodings = fr.face_encodings(face)
                if encodings:  # Check if face encodings were found
                    encoding = encodings[0]
                    encoded[f.split(".")[0]] = encoding
    return encoded

def unknown_image_encoded(img):
    face = fr.load_image_file("faces/" + img)
    encodings = fr.face_encodings(face)
    if encodings:  # Check if face encodings were found
        return encodings[0]
    return None

def classify_face(im):
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)

    face_locations = fr.face_locations(img)
    unknown_face_encodings = fr.face_encodings(img, face_locations)

    face_names = []

    for face_encoding in unknown_face_encodings:
        matches = fr.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        face_distances = fr.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

            cv2.rectangle(img, (left-20, bottom-15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)

            font = cv2.FONT_HERSHEY_DUPLEX

            cv2.putText(img, name, (left-20, bottom+15), font, 1.0, (255, 255, 255), 2)

    while True:
        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    return face_names

print(classify_face("test.jpeg"))
