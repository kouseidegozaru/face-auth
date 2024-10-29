from django.test import TestCase
from django.contrib.auth import get_user_model
from recognizer.models import TrainingData, TrainingGroup
from ..tools.image_generator import generate_random_image
import os

class TestTrainingData(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)
        self.random_image = generate_random_image()
        self.training_data = TrainingData.objects.create(
            group=self.group,
            image=self.random_image,
            label='test_label'
        )
        self.image_path = self.training_data.image.path

    def tearDown(self):
        # テスト終了後に生成された画像ファイルを削除
        if self.training_data.image:
            if self.image_path:
                if os.path.isfile(self.image_path):
                    os.remove(self.image_path)

    def test_create(self):
        self.assertEqual(TrainingData.objects.count(), 1)

    def test_owner(self):
        self.assertEqual(self.training_data.group.owner, self.user)

    def test_group(self):
        self.assertEqual(self.training_data.group, self.group)

    def test_image(self):
        self.assertEqual(self.training_data.image.name, self.random_image.name)

    def test_image_path(self):
        self.assertEqual(self.training_data.image.path, self.image_path)

    def test_label(self):
        self.assertEqual(self.training_data.label, 'test_label')

    def test_update_label(self):
        self.training_data.label = 'updated_label'
        self.training_data.save()
        self.assertEqual(self.training_data.label, 'updated_label')

    def test_update_image(self):
        updated_image = generate_random_image("updated_image.png")
        self.training_data.image = updated_image
        self.training_data.save()
        self.assertEqual(self.training_data.image.name, "updated_image.png")

    def test_delete(self):
        self.training_data.delete()
        self.assertEqual(TrainingData.objects.count(), 0)