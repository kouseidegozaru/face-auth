from ..models import TrainingGroup, FeatureData
from ..services.recognize.feature_models import FeatureModel, FeatureModelStorage


"""
特徴モデルの学習と保存
"""
def feature_model_to_binary(feature_model : FeatureModel) -> bytes:

    # 特徴モデルをバイナリ形式に変換
    feature_storage = FeatureModelStorage()
    feature_storage.set_model(feature_model)
    return feature_storage.convert_to_binary()

def save_feature_model(feature_model : FeatureModel, group : TrainingGroup):

    # 特徴モデルをバイナリ形式に変換
    binary_feature = feature_model_to_binary(feature_model)

    # 保存対象のインスタンスを取得
    feature_file = FeatureData.objects.get(group=group)

    # データを更新
    feature_file.feature = binary_feature
    feature_file.save()