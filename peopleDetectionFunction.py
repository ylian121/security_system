import numpy as np
import cv2

def detect_people(video_source=0, window_size=(640, 480), win_stride=(8, 8)):
    # HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Load Camera or Video
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # resizing
        frame = cv2.resize(frame, window_size)
        # using a greyscale picture
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        boxes, weights = hog.detectMultiScale(frame, winStride=win_stride)

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        if len(boxes) > 0:
            # If a person is detected, return True
            cap.release()
            cv2.destroyAllWindows()
            return True

        for (xA, yA, xB, yB) in boxes:
            # display the detected people
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

        cv2.imshow("Frame", frame)

        k = cv2.waitKey(30) & 0xff

        if k == 27:
            break

    # Release the capture and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Return False if no person is detected
    return False
