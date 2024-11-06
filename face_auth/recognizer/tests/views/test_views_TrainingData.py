from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from allauth.account.models import EmailAddress
from recognizer.models import TrainingData, TrainingGroup
import os
import uuid


class TestTrainingDataViewSet(APITestCase):
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
        # テスト用のTrainingDataの作成
        self.training_data = TrainingData.objects.create(
            group=self.group,
            label='test_label',
            image=SimpleUploadedFile("test_image.jpg", b"random_image_data", content_type="image/jpeg")
        )
        # 作成した画像パスを保持
        self.image_paths = [self.training_data.image.path]


    def tearDown(self):
        # 作成した画像ファイルの削除
        for path in self.image_paths:
            if os.path.exists(path):
                os.remove(path)

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

    def test_update_training_data(self):
        # TrainingDataの更新テスト
        url = reverse('training-data-detail', args=[self.training_data.pk])
        data = {
            'label': 'test_label2',
            'image': SimpleUploadedFile("updated_image.jpg", b"updated_image_data", content_type="image/jpeg")
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
        another_user = get_user_model().objects.create_user(
            email='test_email2@example2.com',
            name='test_user2',
            password='test_password',
        )
        self.client.force_authenticate(user=another_user)
        
        # 他のユーザーでのGETアクセスをテスト
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 他のユーザーでのPATCHアクセスをテスト
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 他のユーザーでのDELETEアクセスをテスト
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        another_user.delete()
