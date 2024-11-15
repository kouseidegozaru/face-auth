from unittest.mock import patch

import numpy as np
from django.contrib.auth import get_user_model
from django.test import TestCase
from recognizer.models import TrainingData, TrainingGroup
from recognizer.services.recognize.feature_models import FeatureModel
from recognizer.services.recognize.recognize import train_feature
from recognizer.services.recognize.types import LearningDataSet
from recognizer.tests.tools.clear_test_data import ClearTrainingDataMixin
from recognizer.tests.tools.image_generator import SimpleUploadedImage


class TestTrain(ClearTrainingDataMixin, TestCase):
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
            image = SimpleUploadedImage(name=f"test{i}.jpg")
            training_data = TrainingData.objects.create(group=self.group, image=image, label=f"test{i}")
            # データセットに追加
            self.dataset.add(f"test{i}", training_data.image.path)

    @patch('recognizer.services.recognize.recognize.detect_face', side_effect=lambda image: image) # 画像をそのまま返す
    @patch('recognizer.services.recognize.recognize.extract_face_feature', return_value=np.random.rand(10))
    def test_train_feature(self, mock_detect_face, mock_extract_face_feature):
        # 学習
        feature_model = train_feature(self.dataset)
        self.assertIsInstance(feature_model, FeatureModel)

    @patch('recognizer.services.recognize.recognize.detect_face', side_effect=lambda image: image)
    @patch('recognizer.services.recognize.recognize.extract_face_feature', return_value=np.random.rand(10))
    def test_train_feature_with_empty_dataset(self, mock_detect_face, mock_extract_face_feature):
        # 空のデータセットの場合、例外を発生させる
        dataset = LearningDataSet()
        with self.assertRaises(ValueError):
            train_feature(dataset)

