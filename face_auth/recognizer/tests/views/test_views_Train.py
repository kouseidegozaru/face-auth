from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from allauth.account.models import EmailAddress
from recognizer.models import TrainingGroup, TrainingData
import numpy as np
import uuid
from unittest.mock import patch
from recognizer.tests.tools.clear_test_data import clear_media
from recognizer.tests.tools.image_generator import get_test_image_as_bytes

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
                "test_image1.jpg", get_test_image_as_bytes(), content_type="image/jpeg"
            )
        )
        self.data2 = TrainingData.objects.create(
            label=' test_data2',
            group=self.group,
            image=SimpleUploadedFile(
                "test_image2.jpg", get_test_image_as_bytes(), content_type="image/jpeg"
            )
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

    def tearDown(self):
        # 削除対象のファイルを削除する
        clear_media()

    @patch('recognizer.services.recognize.recognize.detect_face', side_effect=lambda image: image)
    @patch('recognizer.services.recognize.recognize.extract_face_feature', return_value=np.random.rand(10))
    @patch('recognizer.services.validations.validations.is_exist_face', return_value=True)
    def test_post(self, mock_is_exist_face, mock_extract_face_feature, mock_detect_face):
        # POSTリクエストのテスト
        url = reverse('train', args=[self.group.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TrainingData.objects.count(), 2)

    def test_post_face_not_found(self):
        # POSTリクエストの失敗テスト
        url = reverse('train', args=[self.group.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('recognizer.services.recognize.recognize.detect_face', side_effect=lambda image: image)
    @patch('recognizer.services.recognize.recognize.extract_face_feature', return_value=np.random.rand(10))
    @patch('recognizer.services.validations.validations.is_exist_face', return_value=True)
    def test_post_group_not_found(self, mock_is_exist_face, mock_extract_face_feature, mock_detect_face):
        # POSTリクエストの失敗テスト
        url = reverse('train', args=[uuid.uuid4()])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('recognizer.services.recognize.recognize.detect_face', side_effect=lambda image: image)
    @patch('recognizer.services.recognize.recognize.extract_face_feature', return_value=np.random.rand(10))
    @patch('recognizer.services.validations.validations.is_exist_face', return_value=True)
    def test_post_data_not_enough(self, mock_is_exist_face, mock_extract_face_feature, mock_detect_face):
        # POSTリクエストの失敗テスト
        self.data1.delete()
        url = reverse('train', args=[self.group.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_get_failed(self):
        # GETリクエストの失敗テスト
        url = reverse('train', args=[self.group.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
