import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

img = cv2.imread('random.jpeg')
#img = cv2.imread('people.jpeg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#the bigger the numbers, the most accurate
faces = face_cascade.detectMultiScale(gray, 1.1, 20)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
