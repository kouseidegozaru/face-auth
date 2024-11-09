from django.test import TestCase
from recognizer.tests.tools.image_generator import get_test_image
from recognizer.services.recognize.recognize import predict_feature
from recognizer.tests.tools.feature_model_generator import get_random_feature_model
from unittest.mock import patch
import numpy as np

class TestPredict(TestCase):
    def setUp(self):
        self.opened_image = get_test_image()
        self.feature_model = get_random_feature_model()

    @patch('face_recognition.face_encodings', return_value=[np.random.rand(10)])
    def test_predict_feature(self, mock_face_encodings):
        feature = predict_feature(self.feature_model, self.opened_image)
        self.assertIsInstance(feature, str)

    @patch('face_recognition.face_encodings', return_value=[np.random.rand(10)])
    def test_predict_feature_no_feature_model(self, mock_face_encodings):
        with self.assertRaises(AttributeError):
            feature = predict_feature(None, self.opened_image)

    @patch('face_recognition.face_encodings', return_value=[np.random.rand(10)])
    def test_predict_feature_no_image(self, mock_face_encodings):
        with self.assertRaises(ValueError):
            feature = predict_feature(self.feature_model, None)
