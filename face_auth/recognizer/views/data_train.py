from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import TrainingGroup
from .logic import feature_training,feature_predict
from ..serializers import TrainSerializer, PredictSerializer
from ..services.tools import open_image

class TrainView(APIView):
    # 認証済みのユーザーのみアクセス可能
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # シリアライザーの初期化とバリデーション
        serializer = TrainSerializer(data={**request.data, 'pk': pk})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # トレーニンググループの取得
        group = get_object_or_404(TrainingGroup, pk=pk)

        # オーナーの確認
        if group.owner != request.user:
            return Response({"detail": "You do not have permission to train this group."}, status=status.HTTP_403_FORBIDDEN)

        # 学習
        feature_training(group.id)
        
        return Response(status=status.HTTP_200_OK)


class PredictView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # シリアライザーの初期化とバリデーション
        serializer = PredictSerializer(data={**request.data, 'pk': pk})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # トレーニンググループの取得
        group = get_object_or_404(TrainingGroup, pk=pk)

        # オーナーの確認
        if group.owner != request.user:
            return Response({"detail": "You do not have permission to predict this group."}, status=status.HTTP_403_FORBIDDEN)

        # 画像の読み込み
        image_data = open_image(serializer.validated_data['image'])
        # 推論
        result_label = feature_predict(group.id, image_data)

        return Response(result_label)
