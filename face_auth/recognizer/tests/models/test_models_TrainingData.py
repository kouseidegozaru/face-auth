from django.test import TestCase
from django.contrib.auth import get_user_model
from recognizer.models import TrainingData, TrainingGroup
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class TestTrainingData(TestCase):
    def setUp(self):
        # テストユーザーの作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        # テスト用のTrainingGroupの作成
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)

        # テスト用のランダム画像をSimpleUploadedFileで生成
        self.random_image = SimpleUploadedFile(
            "test_image.jpg", b"random_image_data", content_type="image/jpeg"
        )
        
        # TrainingDataインスタンスの作成
        self.training_data = TrainingData.objects.create(
            group=self.group,
            image=self.random_image,
            label='test_label'
        )
        
        # 削除対象のファイルパスを保持するリスト
        self.image_paths = [self.training_data.image.path]

    def tearDown(self):
        # テスト終了後に生成されたすべての画像ファイルを削除
        for path in self.image_paths:
            if os.path.isfile(path):
                os.remove(path)

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
        # TrainingDataの画像ファイル名が正しいか確認
        self.assertEqual(os.path.basename(self.training_data.image.name), "test_image.jpg")

    def test_image_path(self):
        # TrainingDataの画像ファイルパスが正しいか確認
        self.assertEqual(self.training_data.image.path, self.image_paths[0])

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
        updated_image = SimpleUploadedFile(
            "updated_image.jpg", b"updated_image_data", content_type="image/jpeg"
        )
        self.training_data.image = updated_image
        self.training_data.save()
        
        # 更新後の画像パスを削除対象リストに追加
        self.image_paths.append(self.training_data.image.path)
        self.assertEqual(os.path.basename(self.training_data.image.name), "updated_image.jpg")

    def test_delete(self):
        # TrainingDataを削除し、データベースから削除されたことを確認
        self.training_data.delete()
        self.assertEqual(TrainingData.objects.count(), 0)
