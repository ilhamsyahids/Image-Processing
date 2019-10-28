
import cv2
import numpy as np
from cv2 import imread
import _pickle as pickle
import random
import os
import matplotlib.pyplot as plt

# Feature extractor


def extract_features(image_path, vector_size=32):
    image = imread(image_path)
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        alg = cv2.KAZE_create()
        # Dinding image keypoints
        kps = alg.detect(image)
        # Getting first 32 of them.
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        kps, dsc = alg.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten()
        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print('Error: ', e)
        return None

    return dsc


def batch_extractor(images_path):
    files = [os.path.join(images_path, p)
             for p in sorted(os.listdir(images_path))]

    result = {}
    for f in files:
        print('Extracting features from image %s' % f)
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)


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
    sample = random.sample(files, 1)

    batch_extractor(images_path)

#     ma = Matcher('features.pck')

    for s in sample:
        print('Query image ==========================================')
        show_img(s)
#         names, match = ma.match(s, topn=3)
#         print( 'Result images ========================================')
#         for i in range(3):
#             # we got cosine distance, less cosine distance between vectors
#             # more they similar, thus we subtruct it from 1 to get match value
#             print ('Match %s' % (1-match[i]))
#             show_img(os.path.join(images_path, names[i]))


run()