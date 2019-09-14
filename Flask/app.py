from flask import Flask
import base64
from PIL import Image
import io
import cv2
import numpy as np
import os
import sys
import requests
import time
app = Flask(__name__)

@app.route("/", methods=["POST"])
def home():
    data = request.json

    image = readb64(data.base64)

    w = 1024

    #image = scale_image(image, 1 / 4)
    height, width = image.shape[:2]
    target_size = (w, round(w * (height / width)))
    image = cv2.resize(image, target_size)
    # Removing Gaussian Noise
    image = cv2.GaussianBlur(image, (3, 3), 0)

    
    result = segment_color_marked(image)

    result = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
    cv2.imwrite('out.jpg', result)
    json = get_ocr(result)
    return "Hello, Flask!"

def readb64(base64_string):
    sbuf = io.StringIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

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
    #image = cv2.bitwise_and(image, image, mask=mask)
    cv2.imwrite('mask_red.jpg', mask)
    #cv2.imwrite('image_masked.jpg', image)
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    mask = create_contours_mask(mask)

    #mask = dilate(mask)

    radius = int(mask.shape[0] * 0.02)
    kernel = np.ones((radius, radius),np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)

    
    cv2.imwrite('mask.jpg', mask)
    #mask_inverted = cv2.bitwise_not(mask)

    result = cv2.bitwise_and(image, image, mask=mask)
    return result
    

def dilate(image):
    radius = int(image.shape[0] * 0.0075)
    kernel = np.ones((radius, radius),np.uint8)

    image = cv2.dilate(image, kernel, iterations=1)
    return image

def scale_image(image, scale):
    height, width = image.shape[:2]
    res = cv2.resize(image, (round(scale * width), round(scale * height)))
    return res


def create_contours_mask(image):
    num_pixels = image.shape[0] * image.shape[1]

    # Applying inverse binary due to white background and adapting thresholding for better results
    block_size = 205
    block_size = int(num_pixels / 10000)
    # force block_size % 2 == 1
    block_size += 1 - block_size % 2
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, 50)

    cv2.imwrite('thresh.jpg', thresh)


    #cv2.imshow("Binary", thresh)

    # Finding contours with simple retrieval (no hierarchy) and simple/compressed end points
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    assert contours, contours

    # An empty list to store filtered contours
    filtered = []


    # If it has significant area, add to list
    filtered = [c for c in contours if cv2.contourArea(c) > (num_pixels * 0.001)]

    assert filtered, contours

    # Initialize an equally shaped image
    mask = np.zeros([image.shape[0], image.shape[1], 1], 'uint8')

    # Looping over filtered contours
    for c in filtered:
        #col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        col = 255
        cv2.drawContours(mask, [c], -1, col, -1)
        #area = cv2.contourArea(c)
        # Fetch the perimeter
        #p = cv2.arcLength(c, True)
        #print(area, p)
    return mask
    

def get_ocr(image):
    v1_url = 'https://aihackathoncomputervision.cognitiveservices.azure.com/vision/v1.0/recognizeText?printed=true'
    v2_url = 'https://aihackathoncomputervision.cognitiveservices.azure.com/vision/v2.0/recognizeText?mode=Printed&language=de'

    url = v2_url

    data = {}
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': 'dfcc1195e70a44d7a4adfde1f075844d'}

    header_key = {'Ocp-Apim-Subscription-Key': 'dfcc1195e70a44d7a4adfde1f075844d'}

    data = cv2.imencode('.png', image)[1]
    r = requests.post(url, headers=headers, data=data.tobytes())
    r.raise_for_status()
    next_url = r.headers['Operation-Location']
    while True:
        time.sleep(1)
        r2 = requests.get(next_url, headers=header_key)
        r2j = r2.json()
        if r2j.get('status', None) != 'Running' and not 'error' in r2j:
            return r2j

