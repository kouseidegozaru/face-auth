from unittest.mock import patch

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.urls import reverse
from recognizer.models import TrainingData, TrainingGroup
from recognizer.tests.tools.clear_test_data import ClearTrainingDataMixin
from recognizer.tests.tools.image_generator import SimpleUploadedImage
from recognizer.tests.views.Auther import AuthTestMixin, CsrfTestMixin
from rest_framework import status
from rest_framework.test import APITestCase


class TestGroupDataViewSet(ClearTrainingDataMixin, APITestCase, AuthTestMixin, CsrfTestMixin):
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
        # テスト用の画像
        self.image = SimpleUploadedImage()

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

