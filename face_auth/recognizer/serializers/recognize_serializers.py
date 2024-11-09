from rest_framework import serializers
from ..models import TrainingGroup, TrainingData
from ..services.validations.validations import is_exist_face
from ..services.tools.image_operations import open_image

def get_object_or_exception(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise serializers.ValidationError(f"{model.__name__} does not exist.")

class TrainSerializer(serializers.Serializer):
    pk = serializers.UUIDField()  # pkはURLパラメータを想定

    def validate(self, data):
        # トレーニンググループの取得
        group = get_object_or_exception(TrainingGroup, pk=data['pk'])
        # トレーニングデータの件数を取得
        training_data_count = TrainingData.objects.filter(group=group).count()

        # グループに画像ファイルが2種類以上あるか
        if training_data_count < 2:
            raise serializers.ValidationError("You must upload at least two images to train this group.")

        return data


class PredictSerializer(serializers.Serializer):
    pk = serializers.UUIDField()  # pkはURLパラメータを想定
    image = serializers.ImageField()

    def validate(self, data):
        # トレーニンググループの取得
        group = get_object_or_exception(TrainingGroup, pk=data['pk'])

        # 特徴モデルが存在するか確認
        if not group.feature_model:
            raise serializers.ValidationError("Feature model does not exist.")

        # 画像の確認
        image_data = open_image(data.get('image'))
        if not is_exist_face(image_data):
            raise serializers.ValidationError("画像に顔が見つかりません")

        return data
