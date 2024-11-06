from rest_framework import serializers
from ..models import TrainingGroup, TrainingData
from ..services.validations.validations import is_exist_face
from ..services.tools.image_operations import open_image


class TrainingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingGroup
        fields = ['id', 'name', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # nameは必須
        if validated_data.get("name") is None:
            raise serializers.ValidationError("detail: 'name' is required")
        return super().update(instance, validated_data)


class TrainingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingData
        fields = ['id', 'group', 'image', 'label', 'created_at', 'updated_at']
        read_only_fields = ['id', 'group', 'created_at', 'updated_at']

    def create(self, validated_data):
        # imageに顔が見つからない場合はエラー
        image = open_image(validated_data.pop('image'))
        if not is_exist_face(image):
            raise serializers.ValidationError("detail: cannot detect face in image")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # imageとlabelのどちらもない場合はエラー
        if validated_data.get("image") is None and validated_data.get("label") is None:
            raise serializers.ValidationError("detail: either 'image' or 'label' must be provided")
        
        # imageに顔が見つからない場合はエラー
        if validated_data.get("image") is not None:
            image = open_image(validated_data["image"])
            if not is_exist_face(image):
                raise serializers.ValidationError("detail: cannot detect face in image")
        
        return super().update(instance, validated_data)
    