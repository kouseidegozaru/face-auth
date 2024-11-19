from django.contrib.auth import get_user_model
from django.test import TestCase
from recognizer.models import TrainingData, TrainingGroup
from recognizer.tests.tools.clear_test_data import ClearTrainingDataMixin
from recognizer.tests.tools.image_generator import SimpleUploadedImage


class TestTrainingData(ClearTrainingDataMixin,TestCase):
    def setUp(self):
        # テストユーザーの作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        # テスト用のTrainingGroupの作成
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)

        # テスト用のランダム画像を生成
        self.random_image = SimpleUploadedImage()
        
        # TrainingDataインスタンスの作成
        self.training_data = TrainingData.objects.create(
            group=self.group,
            image=self.random_image,
            label='test_label'
        )

    def test_create(self):
        # TrainingDataが1件作成されていることを確認
        self.assertEqual(TrainingData.objects.count(), 1)

    def test_owner(self):
        # TrainingDataが属するTrainingGroupのオーナーが正しいユーザーであることを確認
        self.assertEqual(self.training_data.group.owner, self.user)

    def test_group(self):
        # 作成したTrainingDataが正しいTrainingGroupに紐付いていることを確認
        self.assertEqual(self.training_data.group, self.group)

    def test_image(self):
        # TrainingDataの画像が登録されているか確認
        self.assertIsNotNone(self.training_data.image)

    def test_image_path(self):
        # TrainingDataの画像ファイルパスが正しいか確認
        created_training_data = TrainingData.objects.get(pk=self.training_data.pk)
        self.assertEqual(self.training_data.image.path, created_training_data.image.path)

    def test_label(self):
        # TrainingDataのラベルが正しいか確認
        self.assertEqual(self.training_data.label, 'test_label')

    def test_update_label(self):
        # ラベルを更新し、正しく反映されているか確認
        self.training_data.label = 'updated_label'
        self.training_data.save()
        self.assertEqual(self.training_data.label, 'updated_label')

    def test_update_image(self):
        # 画像を更新し、新しい画像ファイル名が正しいか確認
        old_name = self.training_data.image.name
        updated_image = SimpleUploadedImage(name="updated_image.jpg")
        self.training_data.image = updated_image
        self.training_data.save()
        self.assertNotEqual(self.training_data.image.name, old_name)

    def test_delete(self):
        # TrainingDataを削除し、データベースから削除されたことを確認
        self.training_data.delete()
        self.assertEqual(TrainingData.objects.count(), 0)
