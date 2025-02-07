import pickle

import numpy as np
from sklearn.neighbors import NearestNeighbors


class PredictResult:
    """推論結果を保持するクラス"""
    def __init__(self, label: str, distance: float):
        self.label = label
        self.distance = distance


class FeatureModel:
    """学習後の特徴モデルを保持するクラス"""

    def __init__(self, model : NearestNeighbors, labels : list[str]):
        self.model = model
        self.labels = labels

    def predict(self, face_feature : np.ndarray) -> PredictResult:
        distances, indices = self.model.kneighbors(face_feature.reshape(1, -1))
        predict_result = PredictResult(self.labels[indices[0][0]], distances[0][0])
        return predict_result
    

class FeatureModelStorage:
    """学習後の特徴モデルをバイナリで保持したり復元したりするクラス"""

    def set_model(self, model: FeatureModel):
        self.model = model

    def set_binary_feature(self, binary_feature: bytes):
        self.model = pickle.loads(binary_feature)

    def get(self) -> FeatureModel:
        return self.model

    def convert_to_binary(self) -> bytes:
        return pickle.dumps(self.model)
