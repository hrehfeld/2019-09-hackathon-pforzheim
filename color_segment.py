import cv2
import numpy as np
import os
import sys

def create_color_marked_mask(image):
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
    return mask
    

def segment_color_marked(image):
    mask = create_color_marked_mask(image)

    mask = dilate(mask)
    cv2.imwrite('mask.jpg', mask)
    #mask_inverted = cv2.bitwise_not(mask)

    result = cv2.bitwise_and(image, image, mask=mask)
    return result
    

def dilate(image):
    radius = int(image.shape[0] * 0.0075)
    print(radius)
    kernel = np.ones((radius, radius),np.uint8)

    image = cv2.dilate(image, kernel, iterations=1)
    return image


if __name__ == '__main__':
    image_filepath = sys.argv[1]
    image = cv2.imread(image_filepath)
    result = segment_color_marked(image)

    cv2.imwrite('out.jpg', result)
