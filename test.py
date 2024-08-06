import cv2
import numpy as np

# Create a black image
image = np.zeros((400, 600, 3), dtype=np.uint8)

# Draw a rectangle
cv2.rectangle(image, (50, 50), (200, 150), (0, 255, 0), 2)

# Draw a circle
cv2.circle(image, (300, 100), 30, (0, 0, 255), -1)

# Display the image
cv2.imshow('Ex', image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
