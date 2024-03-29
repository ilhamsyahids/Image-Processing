import cv2
import numpy as np
import scipy
from cv2 import imread
import pickle
import random
import os
import matplotlib.pyplot as plt
from math import sqrt
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


def batch_extractor(images_path, pickled_db_path="image_features.pck"):
    files = [os.path.join(images_path, p)
             for p in sorted(os.listdir(images_path))]

    result = {}
    for f in files:
        print('Extracting features from image %s' % f)
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)

    # saving all our feature vectors in pickled file
    with open(pickled_db_path, 'wb') as fp:
        pickle.dump(result, fp)


class Matcher(object):

    def __init__(self, pickled_db_path="features.pck"):
        with open(pickled_db_path, 'rb') as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def cos_cdist(self, vector):
        array_cos = []
        for i in range(len(self.matrix)):
            array_cos.append(1 - self.compareCosine(vector, self.matrix[i]))
        return np.array(array_cos)

    def euclidean(self, vector):
        array_euclid = []
        for i in range(len(self.matrix)):
            array_euclid.append(self.compareEuclidean(vector, self.matrix[i]))
        return np.array(array_euclid)

    def compareEuclidean(self, vector1, vector2):
        dist = 0
        for i in range(len(vector1)):
            dist += (vector1[i] - vector2[i])**2
        return sqrt(dist)

    def compareCosine(self, vector1, vector2):
        cos_angle = self.dot(vector1, vector2)
        cos_angle /= (self.norm(vector1) * self.norm(vector2))
        return (cos_angle)

    def dot(self, vector1, vector2):
        power = 0
        for i in range(len(vector1)):
            power += (vector1[i] * vector2[i])
        return (power)

    def norm(self, vector):
        value = 0
        for i in range(len(vector)):
            value += (vector[i])**2
        return sqrt(value)

    def match(self, image_path, topn=5):
        features = extract_features(image_path)
        img_distances = self.cos_cdist(features)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()


def show_img(path):
    img = imread(path)
    plt.imshow(img)
    plt.show()


def run():
    images_path = 'resources/images/'
    files = [os.path.join(images_path, p)
             for p in sorted(os.listdir(images_path))]
    # getting 3 random images
    sample = random.sample(files, 3)

    batch_extractor(images_path)

    ma = Matcher('image_features.pck')

    # for s in sample:
    #     print('Query image ==========================================')
    #     show_img(s)
    #     names, match = ma.match(s, topn=3)
    #     print('Result images ========================================')
    #     for i in range(3):
    #         # we got cosine distance, less cosine distance between vectors
    #         # more they similar, thus we subtruct it from 1 to get match value
    #         print('Match %s' % (1-match[i]))
    #         show_img(os.path.join(images_path, names[i]))


run()
