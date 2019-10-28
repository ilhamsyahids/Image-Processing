import cv2
import numpy as np
from cv2 import imread
from scipy import spatial
import scipy
import os
from math import sqrt

from Extract_Features import extract_features


class Matcher(object):
    def __init__(self, images_path):
        files = [os.path.join(images_path, p)
                 for p in sorted(os.listdir(images_path))]
        result = {}
        for f in files:
            # print('Extracting features from image %s' % f)
            name = f.split('/')[-1].lower()
            result[name] = extract_features(f)

        self.data = result
        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def cosine(self, vector):
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

    def match(self, image_path, topn=10, method='cosine'):
        features = extract_features(image_path)
        if (method == 'cosine'):
            img_distances = self.cosine(features)
        else:
            img_distances = self.euclidean_dist(features)

        # getting top 10 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()
