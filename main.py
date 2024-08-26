# use function from user_user
# function to get new user and test
from new_user import capture_new_user, facial_recognition
from delete_user import delete_user
from faceRec import face_recognition
from peopleDetectionFunction import detect_people

import cv2
import os
from simple_facerec import SimpleFacerec

# runs until exit
# can constantly add new users into the system
while True:

    # option for the user to pick
    print("Choose an option:")
    print("1. Add a new user")
    print("2. Start live face recognition monitoring")
    print("3. Delete a recognized user")
    print("4. Exit")

    # getting input
    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        # getting new user
        capture_new_user()
        # testing to see if new user is added
        facial_recognition()
    elif choice == "2":
        #check for person
        detect_people()
        # live time face recognition
        face_recognition()
    elif choice == "3":
        # deleting a recognized user
        delete_user()
        # testing to see if user is deleted
        facial_recognition()
    elif choice == "4":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please try again.")
        

