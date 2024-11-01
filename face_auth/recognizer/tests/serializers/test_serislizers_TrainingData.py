from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import TrainingData, TrainingGroup
from ...serializers.models_serializers import TrainingDataSerializer
from rest_framework.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
import os


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
                "test_image.jpg", b"random_image_data", content_type="image/jpeg"
            ),
            label='test_label'
        )

        # 削除対象のファイルパスを保持するリスト
        self.image_paths = [self.training_data.image.path]

    def tearDown(self):
        # テスト終了後に生成されたすべての画像ファイルを削除
        for path in self.image_paths:
            if os.path.exists(path):
                os.remove(path)

    def test_create(self):
        # シリアライザーの作成テスト
        serializer = TrainingDataSerializer(data={
            "group": self.group,
            "image": SimpleUploadedFile(
                "test_image.jpg", b"random_image_data", content_type="image/jpeg"
            ),
            "label": "test_label"
        })
        self.assertTrue(serializer.is_valid()) # データの検証
        training_data = serializer.save(owner=self.user)
        # テスト用のTrainingDataインスタンスと一致することを確認
        self.assertEqual(training_data.group, self.group)
        self.assertEqual(training_data.image.name, "test_image.jpg")
        self.assertEqual(training_data.label, "test_label")
        self.assertIsNotNone(training_data.created_at)
        self.assertIsNotNone(training_data.updated_at)

    def test_update_label(self):
        # シリアライザーの更新テスト
        serializer = TrainingDataSerializer(instance=self.training_data, data={
            "label": "updated_label"
        })
        self.assertTrue(serializer.is_valid())
        updated_training_data = serializer.save()
        self.assertEqual(updated_training_data.label, "updated_label")

    def test_update_fail_label_required(self):
        # シリアライザーのlabel更新失敗テスト
        serializer = TrainingDataSerializer(instance=self.training_data, data={})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        self.assertIn("label", str(context.exception))

    def test_update_image(self):
        # シリアライザーの更新テスト
        image = SimpleUploadedFile(
            "updated_image.jpg", b"updated_image_data", content_type="image/jpeg"
        )
        serializer = TrainingDataSerializer(instance=self.training_data, data={
            "image": image
        })
        self.assertTrue(serializer.is_valid())
        updated_training_data = serializer.save()
        self.assertEqual(updated_training_data.image.name, "updated_image.jpg")
        
        # 削除対象のファイルパスを保持するリストに追加
        self.image_paths.append(updated_training_data.image.path)

    def test_update_fail_image_required(self):
        # シリアライザーのimage更新失敗テスト
        serializer = TrainingDataSerializer(instance=self.training_data, data={})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        self.assertIn("image", str(context.exception))

    def test_update_fail_group_read_only(self):
        # シリアライザーのgroup更新失敗テスト(groupは読み取り専用)
        serializer = TrainingDataSerializer(instance=self.training_data, data={
            "group": self.group,
            "label": "updated_label"
        })
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        self.assertIn("group", str(context.exception))

    def test_update_fail_owner_read_only(self):
        # シリアライザーのowner更新失敗テスト(ownerは読み取り専用)
        serializer = TrainingDataSerializer(instance=self.training_data, data={
            "group": self.group,
            "label": "updated_label"
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("owner", serializer.errors)
