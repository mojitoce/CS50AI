from sys import argv
import os
import cv2
import numpy as np


NUM_CATEGORIES = 3
IMG_WIDTH = 30
IMG_HEIGHT = 30
script, dir = argv

sub_dir = [str(i) for i in range(NUM_CATEGORIES)]

print(dir)
print(sub_dir)

images = []
labels = []
dsize = (IMG_WIDTH, IMG_HEIGHT)

for i in range(NUM_CATEGORIES):
    cat_path = os.path.join(dir, str(i))
    for im_name in os.listdir(cat_path):
        im = cv2.imread(os.path.join(cat_path, im_name), -1)
        im_res = cv2.resize(im, dsize = (IMG_WIDTH, IMG_HEIGHT))

        images.append(im_res)
        labels.append(i)
        break
    break


print(im_res.shape)
