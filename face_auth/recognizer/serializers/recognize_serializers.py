from recognizer.models import TrainingGroup
from recognizer.services.tools.image_operations import open_image
from recognizer.services.validations.validations import is_exist_face
from rest_framework import serializers


def get_object_or_exception(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise serializers.ValidationError(f"{model.__name__} does not exist.")

class TrainSerializer(serializers.Serializer):
    pk = serializers.UUIDField()  # pkはURLパラメータを想定

    def validate(self, data):
        # トレーニンググループの取得
        is_exist_group = TrainingGroup.objects.filter(pk=data['pk']).exists()

        # トレーニンググループが存在するか確認
        if not is_exist_group:
            raise serializers.ValidationError("TrainingGroup does not exist.")

        return data


class PredictSerializer(serializers.Serializer):
    pk = serializers.UUIDField()  # pkはURLパラメータを想定
    image = serializers.ImageField()

    def validate(self, data):
        # トレーニンググループの取得
        is_exist_group = TrainingGroup.objects.filter(pk=data['pk']).exists()

        # トレーニンググループが存在するか確認
        if not is_exist_group:
            raise serializers.ValidationError("TrainingGroup does not exist.")

        # 画像の確認
        image_data = open_image(data.get('image'))
        if not is_exist_face(image_data):
            raise serializers.ValidationError("画像に顔が見つかりません")

        return data
