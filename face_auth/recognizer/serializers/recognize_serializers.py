from rest_framework import serializers
import uuid

from ..services.validations import is_exist_face
from ..services.tools import open_image

class PredictSerializer(serializers.Serializer):
    pk = serializers.UUIDField()  # pkはURLパラメータを想定
    image = serializers.ImageField()

    def validate(self, data):
            image_data = open_image(data.get('image'))
            if not is_exist_face(image_data):
                raise serializers.ValidationError("画像に顔が見つかりません")
            
            return data
    
    