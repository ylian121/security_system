import cv2
import face_recognition

img = cv2.imread("bill.jpg")
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_encoding = face_recognition.face_encodings(rgb_img)[0]

img2 = cv2.imread("bill2.jpg")
rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]

img3 = cv2.imread("obama.jpg")
rgb_img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
img_encoding3 = face_recognition.face_encodings(rgb_img3)[0]

result = face_recognition.compare_faces([img_encoding], img_encoding3)
print("Result: ", result)

cv2.imshow("img", img)
cv2.imshow("img", img2)
cv2.imshow("img", img3)


