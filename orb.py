import numpy as np
import cv2
from matplotlib import pyplot as plt
import numpy as np

img = cv2.imread('images/IMG_20190914_143840.jpg')

image_size = img.shape[:2]
print(image_size)
crop_size = image_size * 0.5
img = img[y:y+h, x:x+w]

# Initiate STAR detector
orb = cv2.ORB_create()

# find the keypoints with ORB
kp = orb.detect(img)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

img2 = img.copy()
# draw only keypoints location,not size and orientation
cv2.drawKeypoints(img, kp, img2, color=(255, 0, 0), flags=0)
plt.imshow(img2)
plt.show()
