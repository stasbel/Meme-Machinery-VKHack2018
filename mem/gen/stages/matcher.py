import numpy as np
from sklearn.neighbors import KDTree

from mem.gen.stages import Embedder


class Matcher:
    def __init__(self, matrix, eps=1e-12):
        self.embedder = Embedder()
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis=0)
        self.eps = eps
        self.model = KDTree((matrix - self.mean) / (self.std + self.eps))

    def match(self, image, top_k=1):
        e = self.embedder.embed(image)
        e = (e - self.mean) / (self.std + self.eps)

        d = self._cos_cdist(e, top_k)

        nearest_ids = d.tolist()

        return nearest_ids

    def _cos_cdist(self, e, top_k):
        return self.model.query(e.reshape(1, -1), k=top_k)[1].reshape(-1)
