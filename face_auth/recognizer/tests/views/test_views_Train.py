from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from recognizer.models import TrainingGroup, TrainingData
import os
import uuid

class TestTrainView(APITestCase):

    def setUp(self):
        # テストユーザーの作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        # テスト用のTrainingGroupの作成
        self.group = TrainingGroup.objects.create(
            name='test_group',
            owner=self.user
        )
        # テスト用のTrainingDataの作成
        self.data = TrainingData.objects.create(
            label=' test_data',
            group=self.group,
            image=SimpleUploadedFile(
                "test_image.jpg", b"random_image_data", content_type="image/jpeg"
            )
        )

        # 削除対象のファイルパスを保持するリスト
        self.image_paths = [self.data.image.path]

        # 認証トークンの取得
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'email': 'test_email@example.com', 'password': 'test_password'},
            format='json'
        )
        self.token = response.data.get('access')
        if not self.token:
            raise ValueError('Token retrieval failed')
        # 認証ヘッダーの設定
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def tearDown(self):
        # 削除対象のファイルを削除する
        for path in self.image_paths:
            if os.path.exists(path):
                os.remove(path)

    def test_post(self):
        # POSTリクエストのテスト
        # テスト用のTrainingDataの作成
        self.data = TrainingData.objects.create(
            label=' test_data',
            group=self.group,
            image=SimpleUploadedFile(
                "test_image.jpg", b"random_image_data", content_type="image/jpeg"
            )
        )
        url = reverse('train', args=[self.group.pk])
        data = {}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrainingData.objects.count(), 2)

    def test_get_failed(self):
        # GETリクエストの失敗テスト
        url = reverse('train', args=[self.group.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
