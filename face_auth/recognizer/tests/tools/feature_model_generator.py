from ...services.recognize.feature_models import FeatureModelStorage, FeatureModel
from sklearn.neighbors import NearestNeighbors
import numpy as np

def get_pre_feature_model() -> FeatureModel:
    """
    テスト用の特徴モデルを生成
    """
    pre_trained_model = NearestNeighbors()
    pre_trained_model.fit(np.array([1,2,3,4,5,6,7,8,9,10]))
    pre_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    feature_model = FeatureModel(pre_trained_model, pre_labels)
    return feature_model

def get_pre_binary_feature_model() -> bytes:
    """
    テスト用の特徴モデルをバイナリ形式で生成
    """
    feature_model = get_pre_feature_model()
    feature_model_storage = FeatureModelStorage()
    feature_model_storage.set_model(feature_model)
    return feature_model_storage.convert_to_binary()

def convert_pre_binary_feature_model_to_feature_model(binary_feature_model: bytes) -> FeatureModel:
    """
    テスト用の特徴モデルをバイナリ形式から特徴モデルに変換
    """
    feature_model_storage = FeatureModelStorage()
    feature_model_storage.set_binary_feature(binary_feature_model)
    return feature_model_storage.get()
