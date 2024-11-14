import uuid
from unittest.mock import patch

import numpy as np
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.urls import reverse
from recognizer.models import TrainingData, TrainingGroup
from recognizer.tests.tools.clear_test_data import ClearTrainingDataMixin
from recognizer.tests.tools.image_generator import SimpleUploadedImage
from recognizer.tests.views.Auther import AuthTestMixin
from rest_framework import status
from rest_framework.test import APITestCase


class TestTrainView(ClearTrainingDataMixin, APITestCase, AuthTestMixin):

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
            image=SimpleUploadedImage(name="test_image1.jpg")
        )
        self.data2 = TrainingData.objects.create(
            label=' test_data2',
            group=self.group,
            image=SimpleUploadedImage(name="test_image2.jpg")
        )

        # ユーザーのメールアドレスを認証済みに設定
        EmailAddress.objects.create(user=self.user, email=self.user.email, verified=True, primary=True)
        # 認証トークンの設定
        self.set_auth_token(self.user, 'test_password')

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
