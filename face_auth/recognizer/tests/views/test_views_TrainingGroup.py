from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.urls import reverse
from recognizer.models import TrainingGroup
from recognizer.tests.views.Auther import AuthTestMixin
from rest_framework import status
from rest_framework.test import APITestCase


class TestTrainingGroupViewSet(APITestCase, AuthTestMixin):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com',
            name='test_user',
            password='test_password',
        )
        self.another_user = get_user_model().objects.create_user(
            email='test_email2@example.com',
            name='test_user2',
            password='test_password2',
        )
        # ユーザーのメールアドレスを認証済みに設定
        EmailAddress.objects.create(user=self.user, email=self.user.email, verified=True, primary=True)
        # 認証トークンの設定
        self.set_auth_token(self.user, 'test_password')
        
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)

    def test_list(self):
        # 全てのTrainingGroupを取得
        url = reverse('training-group-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve(self):
        # 特定のTrainingGroupを取得
        url = reverse('training-group-detail', args=[self.group.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_group')

    def test_create(self):
        # TrainingGroupを作成
        url = reverse('training-group-list')
        response = self.client.post(url, data={'name': 'test_group2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrainingGroup.objects.count(), 2)

    def test_update_name_success(self):
        # TrainingGroupを更新
        url = reverse('training-group-detail', args=[self.group.pk])
        response = self.client.patch(url, data={'name': 'test_group2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.group.refresh_from_db()
        self.assertEqual(self.group.name, 'test_group2')

    def test_update_name_failed(self):
        # TrainingGroupを更新
        url = reverse('training-group-detail', args=[self.group.pk])
        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_owner_failed(self):
        # TrainingGroupのオーナーを別のユーザーに更新
        url = reverse('training-group-detail', args=[self.group.pk])
        response = self.client.patch(url, data={'owner': self.another_user})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy(self):
        # TrainingGroupを削除
        url = reverse('training-group-detail', args=[self.group.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TrainingGroup.objects.count(), 0)

    def test_unauthorized_user_access(self):
        # 他のユーザーによるアクセス制限テスト
        url = reverse('training-group-detail', args=[self.group.pk])
        
        self.client.force_authenticate(user=self.another_user)

        # 他のユーザーでのGETアクセスをテスト
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 他のユーザーでのPOSTアクセスをテスト
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 他のユーザーでのPATCHアクセスをテスト
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 他のユーザーでのDELETEアクセスをテスト
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
