from django.test import TestCase
from face_auth.recognizer.tests.tools.image_generator import get_test_image
from recognizer.services.recognize.recognize import predict_feature
from recognizer.tests.tools.feature_model_generator import get_random_feature_model

class TestPredict(TestCase):
    def setUp(self):
        self.opened_image = get_test_image()

        self.feature_model = get_random_feature_model(self.feature_model, self.opened_image)

    def test_predict_feature(self):
        feature = predict_feature()
        self.assertIsInstance(feature, str)

    def test_predict_feature_no_feature_model(self):
        with self.assertRaises(ValueError):
            feature = predict_feature(None, self.opened_image)

    def test_predict_feature_no_image(self):
        with self.assertRaises(ValueError):
            feature = predict_feature(self.feature_model, None)
