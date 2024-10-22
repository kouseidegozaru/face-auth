from rest_framework import serializers
from .models import TrainingGroup, TrainingData, FeatureData

class TrainingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingGroup
        fields = ['id', 'name', 'owner', 'created_at', 'updated_at']  # 必要なフィールドを指定
        read_only_fields = ['id', 'created_at', 'updated_at']  # 自動的に生成されるフィールドを読み取り専用にする

        def update(self, instance, validated_data):
            # ownerの更新を無効にするため、validated_dataからownerを削除
            validated_data.pop('owner', None)  # ownerが含まれていても無視
            return super().update(instance, validated_data)
        

class TrainingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingData
        fields = ['id', 'group', 'image', 'label', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

        def update(self, instance, validated_data):
            # groupの更新を無効にするため、validated_dataからgroupを削除
            validated_data.pop('group', None)  # groupが含まれていても無視
            return super().update(instance, validated_data)
        

class FeatureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureData
        fields = ['id', 'group', 'feature', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        