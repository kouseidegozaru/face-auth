from rest_framework import serializers
from ..models import TrainingGroup, TrainingData
from ..services.validations import is_exist_face
from ..services.tools import open_image


class TrainingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingGroup
        fields = ['id', 'name', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # nameは必須
        if "name" not in validated_data:
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
        if "image" not in validated_data and "label" not in validated_data:
            raise serializers.ValidationError("detail: either 'image' or 'label' must be provided")
        
        # imageに顔が見つからない場合はエラー
        if "image" in validated_data:
            image = open_image(validated_data["image"])
            if not is_exist_face(image):
                raise serializers.ValidationError("detail: cannot detect face in image")
        
        return super().update(instance, validated_data)
    