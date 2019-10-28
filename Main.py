import cv2
import numpy as np
from cv2 import imread
import random
import os
import matplotlib.pyplot as plt

from Matcher import Matcher


def show_img(path):
    img = imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.show()


def run():
    images_path = 'resources/images/'
    files = [os.path.join(images_path, p)
             for p in sorted(os.listdir(images_path))]
    # getting 3 random images
    sample = random.sample(files, 2)

    ma = Matcher(images_path)

    for s in sample:
        print('Query image ==========================================')
        # show_img(s)
        names, match = ma.match(s, topn=10)
        print('Result images ========================================')
        for i in range(10):
            # we got cosine distance, less cosine distance between vectors
            # more they similar, thus we subtruct it from 1 to get match value
            print('Match %s' % (1-match[i]))
            # show_img(os.path.join(images_path, names[i]))


run()
