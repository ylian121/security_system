# use function from user_user
# function to get new user and test
from new_user import capture_new_user, facial_recognition
from faceRec import face_recognition

import cv2
import os
from simple_facerec import SimpleFacerec

while True:

    # option for the user to pick
    print("Choose an option:")
    print("1. Add a new user")
    print("2. Start live face recognition monitoring")
    print("3. Exit")

    # getting input
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        # getting new user
        capture_new_user()
        # testing to see if new user is added
        facial_recognition()
    elif choice == "2":
        # live time face recognition
        face_recognition()
    elif choice == "3":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please try again.")
        

