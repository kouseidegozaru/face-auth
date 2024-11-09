from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import TrainingGroup
from ..repository.save_model import save_feature_model
from ..repository.load_model import load_feature_model
from ..repository.datasets import create_training_data_set
from ..serializers.recognize_serializers import TrainSerializer, PredictSerializer
from ..services.tools.image_operations import open_image
from ..services.recognize.recognize import train_feature, predict_feature

class TrainView(APIView):
    # 認証済みのユーザーのみアクセス可能
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # シリアライザーの初期化とバリデーション
        serializer = TrainSerializer(data={**request.data, 'pk': pk})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # トレーニンググループの取得
        group = get_object_or_404(TrainingGroup, pk=pk, owner=request.user)
        # データセットの作成
        dataset = create_training_data_set(group)
        # 学習
        feature_model = train_feature(dataset)
        # モデルの保存
        save_feature_model(feature_model, group)
        
        return Response(status=status.HTTP_200_OK)


class PredictView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # シリアライザーの初期化とバリデーション
        serializer = PredictSerializer(data={**request.data, 'pk': pk})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # トレーニンググループの取得
        group = get_object_or_404(TrainingGroup, pk=pk, owner=request.user)  
        # 画像の読み込み
        image_data = open_image(serializer.validated_data['image'])
        # 特徴モデルの読み込み
        feature_model = load_feature_model(group.id)
        # 推論
        result_label = predict_feature(feature_model, image_data)

        return Response(result_label)
