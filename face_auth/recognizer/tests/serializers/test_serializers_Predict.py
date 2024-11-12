from django.test import TestCase
from django.contrib.auth import get_user_model
from recognizer.models import TrainingGroup
from recognizer.serializers.recognize_serializers import PredictSerializer
from recognizer.tests.tools.image_generator import get_test_image_as_bytes
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
        self.group = TrainingGroup.objects.create(
            name="test_group",
            owner=self.user,
        )

        # テスト用の画像データを作成
        self.image = SimpleUploadedFile("test_image.jpg", get_test_image_as_bytes(), content_type="image/jpeg")

    @patch('recognizer.services.validations.validations.is_exist_face', return_value=True)
    def test_validate_success(self, mock_is_exist_face):
        # 正常な画像とモデルがある場合の検証
        serializer = PredictSerializer(data={'pk': self.group.pk, 'image': self.image})
        # シリアライザーが正常に検証されることを確認
        self.assertTrue(serializer.is_valid())

    @patch('recognizer.services.validations.validations.is_exist_face', return_value=True)
    def test_validate_fail_no_group(self, mock_is_exist_face):
        # 存在しないトレーニンググループの検証
        serializer = PredictSerializer(data={'pk': uuid.uuid4(), 'image': self.image})
        self.assertFalse(serializer.is_valid())
        self.assertIn("group", serializer.errors)

    @patch('recognizer.services.validations.validations.is_exist_face', return_value=False)
    def test_validate_fail_no_face_in_image(self, mock_is_exist_face):
        # 画像に顔が含まれていない場合
        serializer = PredictSerializer(data={'pk': self.group.pk, 'image': self.image})
        self.assertFalse(serializer.is_valid())
        self.assertIn("画像に顔が見つかりません", serializer.errors)
