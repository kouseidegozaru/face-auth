from django.test import TestCase
from django.contrib.auth import get_user_model

from recognizer.services.recognize.feature_models import FeatureModel
from recognizer.models import TrainingGroup, FeatureData
from recognizer.tests.tools.feature_model_generator import get_random_feature_model, convert_bynary_to_feature_model, convert_to_binary_feature_model


class TestTrainingGroup(TestCase):
    def setUp(self):
        # テストユーザーを作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com',
            name='test_user',
            password='test_password',
        )
        # テスト用のTrainingGroupインスタンスを作成し、ユーザーをオーナーとして設定
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)
        # ランダムなFeatureModelを生成
        self.feature_model: FeatureModel = get_random_feature_model()
        # FeatureModelをバイナリ形式に変換
        self.binary_feature_model: bytes = convert_to_binary_feature_model(self.feature_model)

        # FeatureDataインスタンスを作成し、バイナリ形式のFeatureModelを保存
        self.feature_data = FeatureData.objects.create(
            group=self.group,
            feature=self.binary_feature_model,
        )

    def test_create(self):
        # FeatureDataが1件作成されていることを確認
        self.assertEqual(FeatureData.objects.count(), 1)

    def test_group(self):
        # 作成したFeatureDataが正しいTrainingGroupに紐付いていることを確認
        self.assertEqual(self.feature_data.group, self.group)

    def test_owner(self):
        # FeatureDataが属するTrainingGroupのオーナーが正しいユーザーであることを確認
        self.assertEqual(self.feature_data.group.owner, self.user)

    def test_feature_model(self):
        # FeatureDataのバイナリデータをFeatureModel形式に変換して、元のFeatureModelと一致するか確認
        binary_feature_model = self.feature_data.feature
        feature_model = convert_bynary_to_feature_model(binary_feature_model)
        self.assertIsInstance(feature_model, FeatureModel)
        self.assertEqual(feature_model.labels, self.feature_model.labels)
        self.assertEqual(feature_model.model.get_params(), self.feature_model.model.get_params())

    def test_update_feature_model(self):
        # FeatureModelを更新し、保存後に更新が反映されていることを確認
        updated_feature_model = get_random_feature_model()
        binary_updated_feature_model = convert_to_binary_feature_model(updated_feature_model)
        self.feature_data.feature = binary_updated_feature_model
        self.feature_data.save()
        self.assertEqual(self.feature_data.feature, binary_updated_feature_model)

    def test_delete(self):
        # FeatureDataを削除し、データベースから削除されたことを確認
        self.feature_data.delete()
        self.assertEqual(FeatureData.objects.count(), 0)
