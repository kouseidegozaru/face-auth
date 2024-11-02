from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from recognizer.models import TrainingGroup, TrainingData
import os
import uuid
# 顔画像であるかをクリアするためのモックを作成
from unittest.mock import patch

"""PredictViewのテスト"""


class TestPredictView(APITestCase):
    def setUp(self):
        # テストユーザーの作成
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        # テスト用のTrainingGroupの作成
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)
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
        if self.token is None:
            raise ValueError('token is None')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        self.url = reverse('predict', args=[self.data.pk])

    def tearDown(self):
        # ファイルの削除
        for path in self.image_paths:
            if os.path.exists(path):
                os.remove(path)

    @patch('recognizer.service.validations.validations.is_exist_face', return_value=True)
    def test_post(self):
        # POSTリクエストのテスト
        # TrainingDataを2つ作成
        TrainingData.objects.create(
            label=' test_data',
            group=self.group,
            image=SimpleUploadedFile(
                "test_image.jpg", b"random_image_data", content_type="image/jpeg"
            )
        )
        TrainingData.objects.create(
            label='test_data2',
            group=self.group,
            image=SimpleUploadedFile(
                "test_image2.jpg", b"random_image_data", content_type="image/jpeg"
            )
        )
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_failed(self):
        # GETリクエストの失敗テスト
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
