from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model 
from django.core.files.uploadedfile import SimpleUploadedFile
from recognizer.models import TrainingGroup, TrainingData
import os
import uuid

class TestGroupDataViewSet(APITestCase):
    def setUp(self):
        # テストユーザーの作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        # テスト用のTrainingGroupの作成
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)
        # 作成した画像パスを保持する変数
        self.image_paths = []
        # APIのURLを生成
        self.url = reverse('group-data', args=[self.group.pk])

        # 認証トークンの取得
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'email': 'test_email@example.com', 'password': 'test_password'},
            format='json'
        )
        self.token = response.data.get('access')

    def tearDown(self):
        # 作成した画像パスを削除
        for path in self.image_paths:
            if path and os.path.exists(path):
                os.remove(path)

    def test_get_group_data(self):
        # テスト用のTrainingDataの作成
        training_data = TrainingData.objects.create(
            group=self.group,
            image=SimpleUploadedFile("test_image.jpg", b"random_image_data", content_type="image/jpeg")
        )
        # 作成した画像パスを保持
        self.image_paths.append(training_data.image.path)
        # APIリクエスト
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        # レスポンスの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['label'], training_data.label)

    def test_create_group_data(self):
        # テスト用のTrainingDataの作成
        training_data = TrainingData.objects.create(
            group=self.group,
            image=SimpleUploadedFile("test_image.jpg", b"random_image_data", content_type="image/jpeg")
        )
        # 作成した画像パスを保持
        self.image_paths.append(training_data.image.path)
        # APIリクエスト
        response = self.client.post(
            self.url,
            {
                'label': 'test_label',
                'image': SimpleUploadedFile("test_image.jpg", b"random_image_data", content_type="image/jpeg")
            },
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        # レスポンスの検証
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrainingData.objects.count(), 2)
        self.assertEqual(TrainingData.objects.get(label='test_label').label, 'test_label')

    def test_unauthorized_user_access(self):
        # 他のユーザーによるアクセス制限テスト
        another_user = get_user_model().objects.create_user(
            email='another_test_email@example.com', 
            name='another_test_user',
            password='another_test_password',
        )
        self.client.force_authenticate(user=another_user)

        # 他のユーザーでのGETアクセスをテスト
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 他のユーザーでのPOSTアクセスをテスト
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
