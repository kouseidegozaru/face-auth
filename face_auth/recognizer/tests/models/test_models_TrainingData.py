from django.test import TestCase
from django.contrib.auth import get_user_model
from recognizer.models import TrainingData, TrainingGroup
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class TestTrainingData(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)

        self.random_image = SimpleUploadedFile(
            "test_image.jpg", b"random_image_data", content_type="image/jpeg"
        )
        
        self.training_data = TrainingData.objects.create(
            group=self.group,
            image=self.random_image,
            label='test_label'
        )
        
        # 削除対象のファイルパスリスト
        self.image_paths = [self.training_data.image.path]

    def tearDown(self):
        # テスト終了後に生成されたすべての画像ファイルを削除
        for path in self.image_paths:
            if os.path.isfile(path):
                os.remove(path)

    def test_create(self):
        self.assertEqual(TrainingData.objects.count(), 1)

    def test_owner(self):
        self.assertEqual(self.training_data.group.owner, self.user)

    def test_group(self):
        self.assertEqual(self.training_data.group, self.group)

    def test_image(self):
        self.assertEqual(self.training_data.image.name, "test_image.jpg")

    def test_image_path(self):
        self.assertEqual(self.training_data.image.path, self.image_paths[0])

    def test_label(self):
        self.assertEqual(self.training_data.label, 'test_label')

    def test_update_label(self):
        self.training_data.label = 'updated_label'
        self.training_data.save()
        self.assertEqual(self.training_data.label, 'updated_label')

    def test_update_image(self):
        updated_image = SimpleUploadedFile(
            "updated_image.jpg", b"updated_image_data", content_type="image/jpeg"
        )
        self.training_data.image = updated_image
        self.training_data.save()
        
        # 更新後の画像パスをリストに追加
        self.image_paths.append(self.training_data.image.path)
        self.assertEqual(self.training_data.image.name, "updated_image.jpg")

    def test_delete(self):
        self.training_data.delete()
        self.assertEqual(TrainingData.objects.count(), 0)
