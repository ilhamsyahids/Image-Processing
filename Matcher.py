import cv2
import numpy as np
from cv2 import imread
from scipy import spatial
import scipy
import os
from math import sqrt
import pickle
from GUI import *
from Extract_Features import extract_features

class Matcher(object):
    def __init__(self, images_path, mode="Extract from files", pckfile="features.pck"):
        global labels
        if (mode == "Extract from files"):
            files = [os.path.join(images_path, p)
                     for p in sorted(os.listdir(images_path))]
            result = {}
            for f in files:
                labels["extract_status"].config(text=('Extracting features from image ".../%s"' % os.path.basename(f)), fg="blue")
                root.update()
                name = f.split('/')[-1].lower()
                result[name] = extract_features(f)
            labels["extract_status"].config(text="Extraction done", fg="green")

            self.data = result
        else:
            with open(pckfile, 'rb') as fp:
                self.data = pickle.load(fp)
            labels["extract_status"].config(text="Extraction loaded from pickle", fg="green")

        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def save(self, path):
        if not path.endswith(".pck"):
            path += ".pck"
        with open(path, 'wb') as fp:
            pickle.dump(self.data, fp)

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
        norm1 = self.norm(vector1)
        norm2 = self.norm(vector2)
        for i in range(len(vector1)):
            dist += (vector1[i]/norm1 - vector2[i]/norm2)**2
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

    def match(self, image_path, topn=10, method=0):
        features = extract_features(image_path)
        if (method == 0):
            img_distances = self.cosine(features)
        else:
            img_distances = self.euclidean(features)

        # getting top 10 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()
