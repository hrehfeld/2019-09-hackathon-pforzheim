import json

import sys

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import cv2
import numpy as np
import math

from matplotlib.path import Path
from matplotlib.patches import PathPatch

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result


filename = sys.argv[1]
image_filename = sys.argv[2]


with open(filename, 'r') as f:
    data = json.load(f)
data = data['recognitionResult']

im = cv2.imread(image_filename)
#angle = data['textAngle']
angle = 0
im = rotateImage(im, angle)
    




# Create figure and axes
fig, axis = plt.subplots()
axis.imshow(im)


def parse_aabb(s):
    aabb = []
    for i in range(0, len(s), 2):
        b = s[i], s[i + 1]
        aabb.append(b)
        
    assert len(aabb) == 4, aabb
    #aabb = [float(x) for x in aabb]
    return aabb

def draw_rect(vertices):
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    path = Path(vertices, codes)
    #axis.add_patch(patches.Rectangle(aabb[:2], *aabb[2:], linewidth=1, edgecolor='r', facecolor='none')
    p = PathPatch(path, facecolor='None', edgecolor='r')
    axis.add_patch(p)

lines = data['lines']
for line in lines:
    line_aabb = parse_aabb(line['boundingBox'])
    draw_rect(line_aabb)

    words = line['words']

    for word in words:
        word_aabb = parse_aabb(word['boundingBox'])
        draw_rect(word_aabb)
        

plt.show()

def tag(name, inner=None, **kwargs):
    return '<{name} {kwargs}>{inner}</{name}>'.format(name=name, inner=inner if inner else '')

#content = []

#content.append(tag('img'

#print(tag('html', tag('body')))


print(math.degrees(data['textAngle']))
