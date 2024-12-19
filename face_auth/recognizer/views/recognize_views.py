from django.shortcuts import get_object_or_404
from recognizer.models import FeatureData, TrainingData, TrainingGroup
from recognizer.repository.datasets import create_training_data_set
from recognizer.repository.load_model import load_feature_model
from recognizer.repository.save_model import save_feature_model
from recognizer.serializers.recognize_serializers import PredictSerializer, TrainSerializer
from recognizer.services.recognize.recognize import predict_feature, train_feature
from recognizer.services.tools.image_operations import open_image
from recognizer.views.permissions import IsGroupOwnerOnly
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.permissions import PostHasCsrfTokenNonGetMethod


class TrainView(APIView):
    # 認証済みのユーザーのみアクセス可能
    permission_classes = [IsAuthenticated, IsGroupOwnerOnly, PostHasCsrfTokenNonGetMethod]

    def post(self, request, pk):
        # シリアライザーの初期化とバリデーション
        request.data['pk'] = pk
        serializer = TrainSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # トレーニンググループの取得
        group = get_object_or_404(TrainingGroup, pk=pk, owner=request.user)

        # グループに画像ファイルが2種類以上あるか
        if TrainingData.objects.filter(group=group).count() < 2:
            return Response("You must upload at least two images to train this group.", status=status.HTTP_412_PRECONDITION_FAILED)
        
        try:
            # データセットの作成
            dataset = create_training_data_set(group)
            # 学習
            feature_model = train_feature(dataset)
            # モデルの保存
            save_feature_model(feature_model, group)
            
            return Response(status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class PredictView(APIView):
    permission_classes = [IsAuthenticated, IsGroupOwnerOnly, PostHasCsrfTokenNonGetMethod]

    def post(self, request, pk):
        # シリアライザーの初期化とバリデーション
        request.data['pk'] = pk
        serializer = PredictSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # トレーニンググループの取得
        group = get_object_or_404(TrainingGroup, pk=pk, owner=request.user)

        # 特徴モデルが存在するか確認
        if not FeatureData.objects.filter(group=group).exists():
            return Response("Feature model does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        try:
            # 画像の読み込み
            image_data = open_image(serializer.validated_data['image'])
            # 特徴モデルの読み込み
            feature_model = load_feature_model(group.id)
            # 推論
            result = predict_feature(feature_model, image_data)
            # JSON形式に変換
            result_json = {"label": result.label, "distance": result.distance}

            return Response(result_json, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
