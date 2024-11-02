from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.exceptions import ValidationError
from recognizer.models import TrainingGroup
from recognizer.serializers.recognize_serializers import PredictSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
import uuid

class TestPredictSerializer(TestCase):

    def setUp(self):
        # テストユーザーとトレーニンググループの設定
        self.user = get_user_model().objects.create_user(
            email='test_user@example.com',
            name='test_user',
            password='test_password',
        )

        # 特徴モデルを持つトレーニンググループの作成
        self.group_with_model = TrainingGroup.objects.create(
            name="test_group_with_model",
            owner=self.user,
            feature_model=True  # モデルが存在することを仮定
        )

        # 特徴モデルがないトレーニンググループの作成
        self.group_without_model = TrainingGroup.objects.create(
            name="test_group_without_model",
            owner=self.user,
            feature_model=False  # モデルが存在しない
        )

        # テスト用の画像データを作成
        self.image = SimpleUploadedFile("test_image.jpg", b"test_image_data", content_type="image/jpeg")

    @patch('services.validations.validations.is_exist_face', return_value=True)
    def test_validate_success(self, mock_is_exist_face):
        # 正常な画像とモデルがある場合の検証
        serializer = PredictSerializer(data={'pk': self.group_with_model.pk, 'image': self.image})
        # シリアライザーが正常に検証されることを確認
        self.assertTrue(serializer.is_valid())

    def test_validate_fail_feature_model_missing(self):
        # 特徴モデルが存在しないグループで予測しようとした場合
        serializer = PredictSerializer(data={'pk': self.group_without_model.pk, 'image': self.image})
        self.assertFalse(serializer.is_valid())
        self.assertIn("Feature model does not exist.", serializer.errors)

    @patch('services.validations.validations.is_exist_face', return_value=False)
    def test_validate_fail_no_face_in_image(self, mock_is_exist_face):
        # 画像に顔が含まれていない場合
        serializer = PredictSerializer(data={'pk': self.group_with_model.pk, 'image': self.image})
        self.assertFalse(serializer.is_valid())
        self.assertIn("画像に顔が見つかりません", serializer.errors)
