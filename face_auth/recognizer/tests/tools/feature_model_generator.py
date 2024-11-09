from ...services.recognize.feature_models import FeatureModelStorage, FeatureModel
from sklearn.neighbors import NearestNeighbors
import numpy as np

def get_random_feature_model() -> FeatureModel:
    """
    テスト用の特徴モデルを生成
    """
    # 二次元の仮データの作成
    pre_features = np.array([[i + k for i in range(10)] for k in range(10)])
    pre_trained_model = NearestNeighbors()
    pre_trained_model.fit(np.array(pre_features))
    pre_labels = [str(i) for i in range(10)]
    feature_model = FeatureModel(pre_trained_model, pre_labels)
    return feature_model
