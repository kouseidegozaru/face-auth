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

def convert_to_binary_feature_model(feature_model: FeatureModel) -> bytes:
    """
    テスト用の特徴モデルをバイナリ形式に変換
    """
    feature_model_storage = FeatureModelStorage()
    feature_model_storage.set_model(feature_model)
    return feature_model_storage.convert_to_binary()

def convert_bynary_to_feature_model(binary_feature_model: bytes) -> FeatureModel:
    """
    テスト用の特徴モデルをバイナリ形式から特徴モデルに変換
    """
    feature_model_storage = FeatureModelStorage()
    feature_model_storage.set_binary_feature(binary_feature_model)
    return feature_model_storage.get()

