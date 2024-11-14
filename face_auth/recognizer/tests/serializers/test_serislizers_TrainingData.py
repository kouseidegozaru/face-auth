from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from recognizer.models import TrainingData, TrainingGroup
from recognizer.serializers.models_serializers import TrainingDataSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from recognizer.tests.tools.clear_test_data import clear_media
from recognizer.tests.tools.image_generator import get_test_image_as_bytes
from unittest.mock import patch


class TestTrainingDataSerializer(TestCase):

    def setUp(self):
        # テストユーザーを作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com',
            name='test_user',
            password='test_password',
        )
        # テスト用のTrainingGroupインスタンスを作成し、ユーザーをオーナーとして設定
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)
        # ランダムなTrainingDataインスタンスを作成
        self.training_data = TrainingData.objects.create(
            group=self.group,
            image=SimpleUploadedFile(
                "test_image.jpg", get_test_image_as_bytes(), content_type="image/jpeg"
            ),
            label='test_label'
        )


    def tearDown(self):
        # テスト終了後に生成されたすべての画像ファイルを削除
        clear_media()

    @patch('recognizer.serializers.models_serializers.is_exist_face', return_value=True)
    def test_create(self, mock_is_exist_face):
        # シリアライザーの作成テスト
        serializer = TrainingDataSerializer(data={
            "group": self.group,
            "image": SimpleUploadedFile(
                "test_image.jpg", get_test_image_as_bytes(), content_type="image/jpeg"
            ),
            "label": "test_label"
        })
        self.assertTrue(serializer.is_valid()) # データの検証
        training_data = serializer.save(group=self.group)
        # テスト用のTrainingDataインスタンスと一致することを確認
        self.assertEqual(training_data.group, self.group)
        self.assertIsNotNone(training_data.image)
        self.assertEqual(training_data.label, "test_label")
        self.assertIsNotNone(training_data.created_at)
        self.assertIsNotNone(training_data.updated_at)

    def test_update_label(self):
        # シリアライザーの更新テスト
        serializer = TrainingDataSerializer(instance=self.training_data, data={
            "label": "updated_label"
        }, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_training_data = serializer.save()
        self.assertEqual(updated_training_data.label, "updated_label")

    def test_update_fail_label_required(self):
        # シリアライザーのlabel更新失敗テスト
        serializer = TrainingDataSerializer(instance=self.training_data, data={}, partial=True)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.save()

    @patch('recognizer.serializers.models_serializers.is_exist_face', return_value=True)
    def test_update_image(self, mock_is_exist_face):
        # シリアライザーの更新テスト
        image = SimpleUploadedFile(
            "updated_image.jpg", get_test_image_as_bytes(), content_type="image/jpeg"
        )
        serializer = TrainingDataSerializer(instance=self.training_data, data={
            "image": image
        }, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_training_data = serializer.save()
        self.assertEqual(os.path.basename(updated_training_data.image.name), "updated_image.jpg")


    def test_update_fail_image_required(self):
        # シリアライザーのimage更新失敗テスト
        serializer = TrainingDataSerializer(instance=self.training_data, data={}, partial=True)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.save()

    def test_update_fail_group_read_only(self):
        # シリアライザーのgroup更新無効テスト(groupは読み取り専用)
        another_group = TrainingGroup.objects.create(name='another_group', owner=self.user)
        serializer = TrainingDataSerializer(instance=self.training_data, data={
            "group": another_group,
            "label": "updated_label"
        }, partial=True)
        self.assertTrue(serializer.is_valid())
        training_data = serializer.save()
        self.assertEqual(training_data.group, self.group)

    def test_update_fail_owner_read_only(self):
        # シリアライザーのowner更新失敗テスト(ownerは読み取り専用)
        serializer = TrainingDataSerializer(instance=self.training_data, data={
            "group": self.group,
            "label": "updated_label"
        }, partial=True)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.save()
