from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from unittest.mock import patch
from recognizer.models import TrainingGroup, TrainingData
from recognizer.services.recognize.recognize import train_feature
from recognizer.services.recognize.feature_models import FeatureModel
from recognizer.services.recognize.types import LearningDataSet
import os
from recognizer.tests.tools.clear_test_data import clear_media
from recognizer.tests.tools.image_generator import get_test_image_as_bytes


class TestTrain(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)

        # データセットの作成
        self.dataset = LearningDataSet()
        for i in range(10):
            # 画像の作成
            image = SimpleUploadedFile(f"test{i}.jpg", get_test_image_as_bytes(), content_type="image/jpeg")
            training_data = TrainingData.objects.create(group=self.group, image=image, label=f"test{i}")
            # データセットに追加
            self.dataset.add(f"test{i}", training_data.image.path)

    def tearDown(self):
        clear_media()

    @patch('recognizer.services.recognize.recognize.detect_face', side_effect=lambda image: image) # 画像をそのまま返す
    def test_train_feature(self, mock_detect_face):
        # 学習
        feature_model = train_feature(self.dataset)
        self.assertIsInstance(feature_model, FeatureModel)

    @patch('recognizer.services.recognize.recognize.detect_face', side_effect=lambda image: image)
    def test_train_feature_with_empty_dataset(self, mock_detect_face):
        # 空のデータセットの場合、例外を発生させる
        dataset = LearningDataSet()
        with self.assertRaises(ValueError):
            train_feature(dataset)

