from ...models import TrainingGroup, FeatureData
from ...services.learning import predict_feature
from ...services.learning.feature_models import FeatureModel, FeatureModelStorage

import numpy as np

def feature_model_from_binary(model_binary: bytes) -> FeatureModel:

    # 特徴モデルをバイナリ形式から復元
    feature_model = FeatureModelStorage()
    feature_model.set_binary_feature(model_binary)
    return feature_model.get()

def feature_predict(training_group_id: int, image : np.ndarray) -> str:

    # 特徴モデルを読み込む
    feature_model_binary = FeatureData.objects.get(group_id=training_group_id).feature
    # 特徴モデルを復元
    feature_model = feature_model_from_binary(feature_model_binary)

    return predict_feature(feature_model, image)
