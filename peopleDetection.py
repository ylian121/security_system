import numpy as np
import cv2
 
# the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


# Load Camera
cap = cv2.VideoCapture(0)


while(True):
    ret, frame = cap.read()

    # resizing
    frame = cv2.resize(frame, (640, 480))
    # using a greyscale picture
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        # display the detected people
        cv2.rectangle(frame, (xA, yA), (xB, yB),(0, 255, 0), 2)
    
    cv2.imshow("Frame", frame)

    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()