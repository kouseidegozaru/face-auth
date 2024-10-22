from sklearn.neighbors import NearestNeighbors
import numpy as np

class FeatureModel:
    """学習後の特徴モデルを保持するクラス"""

    def __init__(self, model : NearestNeighbors, labels : list[str]):
        self.model = model
        self.labels = labels

    def predict(self, face_feature : np.ndarray) -> str:
        distances, indices = self.model.kneighbors(face_feature.reshape(1, -1))
        return self.labels[indices[0][0]]
    
