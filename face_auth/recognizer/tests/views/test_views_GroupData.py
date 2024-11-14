from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from allauth.account.models import EmailAddress
from recognizer.models import TrainingGroup, TrainingData
import os
from recognizer.tests.tools.clear_test_data import clear_media
from recognizer.tests.tools.image_generator import get_test_image_as_bytes
from unittest.mock import patch
from recognizer.tests.views.Auther import AuthTestMixin

class TestGroupDataViewSet(APITestCase, AuthTestMixin):
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
        # テスト用のTrainingGroupの作成
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)
        # テスト用の画像
        self.image = SimpleUploadedFile("test_image.jpg", get_test_image_as_bytes(), content_type="image/jpeg")

    def tearDown(self):
        # 作成した画像パスを削除
        clear_media()

    @patch('recognizer.serializers.models_serializers.is_exist_face', return_value=True)
    def test_create_group_data(self, mock_is_exist_face):
        # テスト用のTrainingDataの作成
        url = reverse('group-data', args=[self.group.id])
        data = {'label': 'test_label', 'image': self.image}
        # APIリクエスト
        response = self.client.post(url, data=data)
        # レスポンスの検証
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrainingData.objects.count(), 1)
        training_data = TrainingData.objects.filter(label='test_label').first()
        self.assertIsNotNone(training_data)
        self.assertEqual(training_data.label, 'test_label')
        

    def test_get_group_data(self):
        # テスト用のTrainingDataの取得
        url = reverse('group-data', args=[self.group.id])
        # テスト用のTrainingDataの作成
        training_data = TrainingData.objects.create(
            group=self.group,
            label='test_label',
            image=self.image
        )
        # APIリクエスト
        response = self.client.get(url)
        # レスポンスの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['label'], training_data.label)

    def test_unauthorized_user_access(self):
        # 他のユーザーによるアクセス制限テスト
        url = reverse('group-data', args=[self.group.id])

        another_user = get_user_model().objects.create_user(
            email='another_test_email@example.com',
            name='another_test_user',
            password='another_test_password',
        )
        self.client.force_authenticate(user=another_user)

        # 他のユーザーでのGETアクセスをテスト
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 他のユーザーでのPOSTアクセスをテスト
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

