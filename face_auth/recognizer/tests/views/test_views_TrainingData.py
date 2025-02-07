import uuid
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


class TestTrainingDataViewSet(ClearTrainingDataMixin, APITestCase, AuthTestMixin, CsrfTestMixin):
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
        # テスト用のTrainingDataの作成
        self.training_data = TrainingData.objects.create(
            group=self.group,
            label='test_label',
            image=SimpleUploadedImage()
        )

    def test_list_training_data(self):
        # TrainingDataの一覧取得テスト
        url = reverse('training-data-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_training_data(self):
        # 特定のTrainingDataの取得テスト
        url = reverse('training-data-detail', args=[self.training_data.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('recognizer.serializers.models_serializers.is_exist_face', return_value=True)
    def test_update_training_data(self, mock_is_exist_face):
        # TrainingDataの更新テスト
        url = reverse('training-data-detail', args=[self.training_data.pk])
        data = {
            'label': 'test_label2',
            'image': SimpleUploadedImage(name='updated_image.jpg')
        }
        response = self.client.patch(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.training_data.refresh_from_db()
        self.assertEqual(self.training_data.label, 'test_label2')

    def test_destroy_training_data(self):
        # TrainingDataの削除テスト
        url = reverse('training-data-detail', args=[self.training_data.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TrainingData.objects.count(), 0)

    def test_destroy_with_invalid_id(self):
        # 無効なIDでのTrainingData削除テスト
        invalid_url = reverse('training-data-detail', args=[uuid.uuid4()])
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_without_authentication(self):
        # 認証なしでのTrainingData削除テスト
        url = reverse('training-data-detail', args=[self.training_data.pk])
        self.client.credentials()  # 認証ヘッダーをクリア
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_access(self):
        # 他のユーザーによるアクセス制限テスト
        url = reverse('training-data-detail', args=[self.training_data.pk])
        another_user = get_user_model().objects.create_user(
            email='test_email2@example2.com',
            name='test_user2',
            password='test_password',
        )
        self.client.force_authenticate(user=another_user)
        
        # 他のユーザーでのGETアクセスをテスト
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 他のユーザーでのPATCHアクセスをテスト
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 他のユーザーでのDELETEアクセスをテスト
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        another_user.delete()
