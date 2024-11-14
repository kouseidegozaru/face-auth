from django.test import TestCase
from recognizer.tests.tools.image_generator import test_image
from recognizer.services.recognize.recognize import predict_feature
from recognizer.tests.tools.feature_model_generator import get_random_feature_model
from unittest.mock import patch
import numpy as np

class TestPredict(TestCase):
    def setUp(self):
        self.opened_image = np.array(test_image())
        self.feature_model = get_random_feature_model()

    @patch('recognizer.services.recognize.recognize.face_recognition.face_encodings', return_value=[np.random.rand(10)])
    def test_predict_feature(self, mock_face_encodings):
        # 推論が成功するか
        feature = predict_feature(self.feature_model, self.opened_image)
        self.assertIsInstance(feature, str)

    @patch('recognizer.services.recognize.recognize.face_recognition.face_encodings', return_value=[np.random.rand(10)])
    def test_predict_feature_no_feature_model(self, mock_face_encodings):
        # 特徴モデルがNoneの場合、例外が発生するか
        with self.assertRaises(AttributeError):
            feature = predict_feature(None, self.opened_image)

    @patch('recognizer.services.recognize.recognize.face_recognition.face_encodings', return_value=[np.random.rand(10)])
    def test_predict_feature_no_image(self, mock_face_encodings):
        # 画像がNoneの場合、例外が発生するか
        with self.assertRaises(ValueError):
            feature = predict_feature(self.feature_model, None)
