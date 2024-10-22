from ...models import TrainingGroup, FeatureData
from ...services.learning import create_training_data_set, learning
from ...services.learning.feature_models import FeatureModel, FeatureModelStorage


def save_feature_model(feature_model : FeatureModel, group : TrainingGroup):

    # joblibで特徴モデルをバイナリ形式に変換
    feature_storage = FeatureModelStorage()
    feature_storage.set_model(feature_model)
    binary_feature = feature_storage.convert_to_binary()

    # 保存対象のインスタンスを取得
    feature_file = FeatureData.objects.get(group=group)

    # データを更新
    feature_file.feature = binary_feature
    feature_file.save()


def feature_training(training_group_id):
    # 学習に必要なデータセットを作成
    train_data_set = create_training_data_set(training_group_id)

    # 学習
    feature_model = learning(train_data_set)

    # 学習後の特徴モデルを保存
    save_feature_model(feature_model, train_data_set.group)
    