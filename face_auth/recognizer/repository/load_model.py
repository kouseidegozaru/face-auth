from recognizer.models import TrainingGroup, FeatureData
from recognizer.services.recognize.feature_models import FeatureModel, FeatureModelStorage

"""
特徴モデルの読み込み
"""
def feature_model_from_binary(model_binary: bytes) -> FeatureModel:

    # 特徴モデルをバイナリ形式から復元
    feature_model = FeatureModelStorage()
    feature_model.set_binary_feature(model_binary)
    return feature_model.get()

def load_feature_model(training_group_id: int) -> FeatureModel:

    # 学習するグループ
    training_group = TrainingGroup.objects.get(id=training_group_id)
    # 特徴モデルを読み込む
    feature_model_binary = FeatureData.objects.get(group=training_group).feature
    # 特徴モデルを復元
    feature_model = feature_model_from_binary(feature_model_binary)
    
    return feature_model
