from rest_framework import serializers
from .models import TrainingGroup

class TrainingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingGroup
        fields = ['id', 'name', 'owner', 'created_at', 'updated_at']  # 必要なフィールドを指定
        read_only_fields = ['id', 'created_at', 'updated_at']  # 自動的に生成されるフィールドを読み取り専用にする