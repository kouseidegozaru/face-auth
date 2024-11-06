from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from allauth.account.models import EmailAddress
from recognizer.models import TrainingGroup, FeatureData
from recognizer.tests.tools.feature_model_generator import get_random_feature_model
from recognizer.repository.save_model import feature_model_to_binary
import os
import uuid
from unittest.mock import patch


class TestPredictView(APITestCase):
    def setUp(self):
        # テストユーザーの作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        # ユーザーのメールアドレスを認証済みに設定
        EmailAddress.objects.create(user=self.user, email=self.user.email, verified=True, primary=True)
        # 認証トークンの取得
        response = self.client.post(
            reverse('custom_login'),
            {'email': 'test_email@example.com', 'password': 'test_password'},
            format='json'
        )
        self.token = response.data.get("key")
        if not self.token:
            raise ValueError('Token retrieval failed')
        # 認証ヘッダーの設定
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # テスト用のTrainingGroupの作成
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)
        
        # テスト用の特徴モデルの作成
        self.feature_model = get_random_feature_model()
        self.binary_feature_model = feature_model_to_binary(self.feature_model)
        # テスト用のFeatureDataの作成
        self.feature_data = FeatureData.objects.create(
            group=self.group,
            feature=self.binary_feature_model,
        )

        # 推論する画像の作成
        self.image = SimpleUploadedFile(
            "test_image.jpg", b"random_image_data", content_type="image/jpeg"
        )

    def tearDown(self):
        # ファイルの削除
        for path in self.image_paths:
            if os.path.exists(path):
                os.remove(path)

    @patch('recognizer.service.validations.validations.is_exist_face', return_value=True)
    def test_post(self):
        # POSTリクエストのテスト
        self.url = reverse('predict', args=[self.group.pk])
        response = self.client.post(self.url, {'image': self.image})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_face_not_found(self):
        # POSTリクエストの失敗テスト
        self.url = reverse('predict', args=[self.group.pk])
        response = self.client.post(self.url, {'image': self.image})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('recognizer.service.validations.validations.is_exist_face', return_value=True)
    def test_post_group_not_found(self):
        # POSTリクエストの失敗テスト
        self.url = reverse('predict', args=[uuid.uuid4()])
        response = self.client.post(self.url, {'image': self.image})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('recognizer.service.validations.validations.is_exist_face', return_value=True)
    def test_post_feature_data_not_found(self):
        # POSTリクエストの失敗テスト
        self.feature_data.delete()
        self.url = reverse('predict', args=[self.group.pk])
        response = self.client.post(self.url, {'image': self.image})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('recognizer.service.validations.validations.is_exist_face', return_value=True)
    def test_post_another_user(self):
        # POSTリクエストの失敗テスト
        self.url = reverse('predict', args=[self.group.pk])
        another_user = get_user_model().objects.create_user(
            email='another_test_email@example.com',
            name='another_test_user',
            password='another_test_password',
        )
        self.client.force_authenticate(user=another_user)
        response = self.client.post(self.url, {'image': self.image})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_failed(self):
        # GETリクエストの失敗テスト
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
