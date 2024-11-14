from django.contrib.auth import get_user_model
from django.test import TestCase
from recognizer.models import TrainingGroup


class TestTrainingGroup(TestCase):
    def setUp(self):
        # テストユーザーの作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        # テスト用のTrainingGroupインスタンスを作成し、ユーザーをオーナーとして設定
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)

    def test_create(self):
        # TrainingGroupの作成に成功するかを確認
        self.assertEqual(TrainingGroup.objects.count(), 1)

    def test_owner(self):
        # TrainingGroupのオーナーが正しいユーザーであることを確認
        self.assertEqual(self.group.owner, self.user)

    def test_update(self):
        # グループ名を更新し、変更が保存されているか確認
        self.group.name = 'updated_group'
        self.group.save()
        self.assertEqual(self.group.name, 'updated_group')

    def test_delete(self):
        # グループを削除し、データベースから削除されたことを確認
        self.group.delete()
        self.assertEqual(TrainingGroup.objects.count(), 0)
