from django.contrib.auth import get_user_model
from django.test import TestCase
from recognizer.models import TrainingGroup
from recognizer.serializers.recognize_serializers import TrainSerializer


class TestTrainSerializer(TestCase):

    def setUp(self):
        # テストユーザーとトレーニンググループの設定
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )

        # トレーニンググループの作成
        self.group = TrainingGroup.objects.create(name="test_group", owner=self.user)


    def test_validate_success(self):
        # 正常なトレーニングシリアライザーの検証
        serializer = TrainSerializer(data={"pk": self.group.pk})
        # シリアライザーが正常に検証されることを確認
        self.assertTrue(serializer.is_valid())

    def test_validate_fail_nonexistent_group(self):
        # 存在しないトレーニンググループの検証
        serializer = TrainSerializer(data={"pk": 9999})
        self.assertFalse(serializer.is_valid())
        self.assertIn("TrainingGroup", *serializer.errors['non_field_errors'])
        