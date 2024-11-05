from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from recognizer.models import TrainingGroup, TrainingData
import os
import uuid
from unittest.mock import patch

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
        self.data1 = TrainingData.objects.create(
            label=' test_data1',
            group=self.group,
            image=SimpleUploadedFile(
                "test_image1.jpg", b"random_image_data", content_type="image/jpeg"
            )
        )
        self.data2 = TrainingData.objects.create(
            label=' test_data2',
            group=self.group,
            image=SimpleUploadedFile(
                "test_image2.jpg", b"random_image_data", content_type="image/jpeg"
            )
        )

        # 削除対象のファイルパスを保持するリスト
        self.image_paths = [self.data1.image.path, self.data2.image.path]

        # 認証トークンの取得
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'email': 'test_email@example.com', 'password': 'test_password'},
            format='json'
        )
        self.token = response.data.get('access')
        if self.token is None:
            raise ValueError('Token retrieval failed')
        # 認証ヘッダーの設定
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def tearDown(self):
        # 削除対象のファイルを削除する
        for path in self.image_paths:
            if os.path.exists(path):
                os.remove(path)

    @patch('recognizer.services.validations.validations.is_exist_face', return_value=True)
    def test_post(self, mock_is_exist_face):
        # POSTリクエストのテスト
        url = reverse('train', args=[self.group.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrainingData.objects.count(), 2)

    def test_post_face_not_found(self):
        # POSTリクエストの失敗テスト
        url = reverse('train', args=[self.group.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('recognizer.services.validations.validations.is_exist_face', return_value=True)
    def test_post_group_not_found(self):
        # POSTリクエストの失敗テスト
        url = reverse('train', args=[uuid.uuid4()])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('recognizer.services.validations.validations.is_exist_face', return_value=True)
    def test_post_data_not_enough(self):
        # POSTリクエストの失敗テスト
        self.data1.delete()
        url = reverse('train', args=[self.group.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_failed(self):
        # GETリクエストの失敗テスト
        url = reverse('train', args=[self.group.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
