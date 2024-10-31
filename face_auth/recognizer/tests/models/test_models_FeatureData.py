from django.test import TestCase
from django.contrib.auth import get_user_model

from ...services.recognize.feature_models import FeatureModel
from recognizer.models import TrainingGroup, FeatureData
from ..tools.feature_model_generator import get_random_feature_model, convert_bynary_to_feature_model, convert_to_binary_feature_model


class TestTrainingGroup(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com',
            name='test_user',
            password='test_password',
        )
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)
        self.feature_model: FeatureModel = get_random_feature_model()
        self.binary_feature_model: bytes = convert_to_binary_feature_model(self.feature_model)

        self.feature_data = FeatureData.objects.create(
            group=self.group,
            feature=self.binary_feature_model,
        )

    def test_create(self):
        self.assertEqual(FeatureData.objects.count(), 1)

    def test_group(self):
        self.assertEqual(self.feature_data.group, self.group)

    def test_owner(self):
        self.assertEqual(self.feature_data.group.owner, self.user)

    def test_feature_model(self):
        binary_feature_model = self.feature_data.feature
        feature_model = convert_bynary_to_feature_model(binary_feature_model)
        self.assertEqual(feature_model, self.feature_model)

    def test_update_feature_model(self):
        updated_feature_model = get_random_feature_model()
        binary_updated_feature_model = convert_to_binary_feature_model(updated_feature_model)
        self.feature_data.feature = binary_updated_feature_model
        self.feature_data.save()
        self.assertEqual(self.feature_data.feature, binary_updated_feature_model)

    def test_delete(self):
        self.feature_data.delete()
        self.assertEqual(FeatureData.objects.count(), 0)
