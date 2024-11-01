from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import TrainingGroup
from ...serializers.models_serializers import TrainingGroupSerializer
from rest_framework.exceptions import ValidationError

class TestTrainingGroupSerializer(TestCase):

    def setUp(self):
        # テストユーザーを作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        # テスト用のTrainingGroupインスタンスを作成し、ユーザーをオーナーとして設定
        self.training_group = TrainingGroup.objects.create(
            name="initial_group", 
            owner=self.user
        )

    def test_create(self):
        # シリアライザーの作成テスト
        serializer = TrainingGroupSerializer(data={"name": "test_group"})
        self.assertTrue(serializer.is_valid()) # データの検証
        group = serializer.save(owner=self.user)
        # テスト用のTrainingGroupインスタンスと一致することを確認
        self.assertEqual(group.name, "test_group")
        self.assertEqual(group.owner, self.user)
        self.assertIsNotNone(group.created_at)
        self.assertIsNotNone(group.updated_at)

    def test_create_fail(self):
        # シリアライザーの作成失敗テスト
        serializer = TrainingGroupSerializer(data={"name": None})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_update(self):
        # シリアライザーの更新テスト
        serializer = TrainingGroupSerializer(instance=self.training_group, data={"name": "updated_group"})
        self.assertTrue(serializer.is_valid())
        updated_group = serializer.save()
        self.assertEqual(updated_group.name, "updated_group")

    def test_update_fail_name_required(self):
        # シリアライザーのname更新失敗テスト
        serializer = TrainingGroupSerializer(instance=self.training_group, data={})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        self.assertIn("name", str(context.exception)) # 正しく例外が発生することを確認

    def test_update_fail_owner_read_only(self):
        # シリアライザーのowner更新失敗テスト(ownerは読み取り専用)
        serializer = TrainingGroupSerializer(instance=self.training_group, data={"name": "updated_group", "owner": self.user})
        self.assertFalse(serializer.is_valid())
        self.assertIn("owner", serializer.errors)
