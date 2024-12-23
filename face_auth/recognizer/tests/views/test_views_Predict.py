import uuid
from unittest.mock import patch

import numpy as np
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.urls import reverse
from recognizer.models import FeatureData, TrainingGroup
from recognizer.repository.save_model import feature_model_to_binary
from recognizer.tests.tools.feature_model_generator import get_random_feature_model
from recognizer.tests.tools.image_generator import SimpleUploadedImage
from recognizer.tests.views.Auther import AuthTestMixin, CsrfTestMixin
from rest_framework import status
from rest_framework.test import APITestCase


class TestPredictView(APITestCase, AuthTestMixin, CsrfTestMixin):
    def setUp(self):
        # テストユーザーの作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        # ユーザーのメールアドレスを認証済みに設定
        EmailAddress.objects.create(user=self.user, email=self.user.email, verified=True, primary=True)
        # 認証トークンの設定
        self.set_auth_token(self.user, 'test_password')
        # csrfトークンの設定
        self.set_csrf_token()
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
        self.image = SimpleUploadedImage()

    @patch('recognizer.serializers.recognize_serializers.is_exist_face', return_value=True)
    @patch('recognizer.services.recognize.recognize.extract_face_feature', return_value=np.random.rand(10))
    def test_post(self, mock_extract_face_feature, mock_is_exist_face):
        # POSTリクエストのテスト
        url = reverse('predict', args=[self.group.pk])
        response = self.client.post(url, {'image': self.image})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_face_not_found(self):
        # POSTリクエストの失敗テスト
        url = reverse('predict', args=[self.group.pk])
        response = self.client.post(url, {'image': self.image})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('recognizer.serializers.recognize_serializers.is_exist_face', return_value=True)
    def test_post_group_not_found(self, mock_is_exist_face):
        # POSTリクエストの失敗テスト
        url = reverse('predict', args=[uuid.uuid4()])
        response = self.client.post(url, {'image': self.image})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('recognizer.serializers.recognize_serializers.is_exist_face', return_value=True)
    def test_post_feature_data_not_found(self, mock_is_exist_face):
        # POSTリクエストの失敗テスト
        self.feature_data.delete()
        url = reverse('predict', args=[self.group.pk])
        response = self.client.post(url, {'image': self.image})
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    @patch('recognizer.serializers.recognize_serializers.is_exist_face', return_value=True)
    def test_post_another_user(self, mock_is_exist_face):
        # POSTリクエストの失敗テスト
        url = reverse('predict', args=[self.group.pk])
        another_user = get_user_model().objects.create_user(
            email='another_test_email@example.com',
            name='another_test_user',
            password='another_test_password',
        )
        self.client.force_authenticate(user=another_user)
        response = self.client.post(url, {'image': self.image})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_failed(self):
        # GETリクエストの失敗テスト
        url = reverse('predict', args=[self.group.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
