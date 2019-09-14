import cv2
import numpy as np
import os
import sys

image_filepath = sys.argv[1]

image = cv2.imread(image_filepath)

image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
 
# Range for lower red
lower_red = np.array([0,120,70])
upper_red = np.array([10,255,255])
mask1 = cv2.inRange(image_hsv, lower_red, upper_red)
 
# Range for upper range
lower_red = np.array([170,120,70])
upper_red = np.array([180,255,255])
mask2 = cv2.inRange(image_hsv, lower_red, upper_red)
 
# Generating the final mask to detect red color
mask = mask1 + mask2

N = int(image.shape[0] * 0.0075)
print(N)
kernel = np.ones((N, N),np.uint8)

mask = cv2.dilate(mask, kernel, iterations=1)


#mask_inverted = cv2.bitwise_not(mask)

res = cv2.bitwise_and(image, image, mask=mask)


cv2.imwrite('out.jpg', res)
