import cv2

human_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

#capture video from cam
cap = cv2.VideoCapture(0)

while True:

    _, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #the bigger the numbers, the most accurate
    humans = human_cascade.detectMultiScale(gray, 1.1, 20)

    for (x, y, w, h) in humans:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('img', img)
    
    k = cv2.waitKey(30) & 0xff

    if k==27:
        break

cap.release()