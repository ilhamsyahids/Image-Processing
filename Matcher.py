import cv2
import numpy as np
from cv2 import imread
from scipy import spatial
import scipy
import os

from Extract_Features import extract_features


class Matcher(object):

    def __init__(self, images_path, pickled_db_path="features.pck"):
        files = [os.path.join(images_path, p)
                 for p in sorted(os.listdir(images_path))]
        result = {}
        for f in files:
            print('Extracting features from image %s' % f)
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

    def cos_cdist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        return scipy.spatial.distance.cdist(self.matrix, v, 'cosine').reshape(-1)

    def match(self, image_path, topn=5):
        features = extract_features(image_path)
        img_distances = self.cos_cdist(features)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()
