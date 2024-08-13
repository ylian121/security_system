import threading

import cv2
from deepface import DeepFace 

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

face_match = {'match': False, 'name': None}

test_img = cv2.imread("test.jpg")
random_img = cv2.imread("random.jpeg")
bill_img = cv2.imread("bill.jpg")
elon_img = cv2.imread("elon.jpg")
obama_img = cv2.imread("obama.jpg")
DeepFace.verify(test_img, random_img, bill_img, obama_img, elon_img)

def check_face(frame, images, result):
    try:
        for name, img in images.items():
            if DeepFace.verify(frame, img.copy())['verified']:
                result['match'] = True
                result['name'] = name
                return
        result['match'] = False
        result['name'] = None
    except ValueError:
        result['match'] = False
        result['name'] = None



while True:
    ret, frame = cap.read()

    images = {
        "Yan": cv2.imread("test.jpg"),
        "Mary": cv2.imread("random.jpeg"),
        "Bill": cv2.imread("bill.jpg"),
        "Elon": cv2.imread("elon.jpg"),
        "Obama": cv2.imread("obama.jpg"),
    }

    if ret:
        if counter % 10 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(), images, face_match)).start()
            except ValueError:
                pass
        counter += 1

        if face_match['match']:
            cv2.putText(frame, f"Match! {face_match['name']}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "No Match!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    
        cv2.imshow("video", frame)

    k = cv2.waitKey(30) & 0xff

    if k==27:
        break

cv2.destroyAllWindows()

