from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from recognizer.models import TrainingGroup


class TestTrainingGroupViewSet(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com',
            name='test_user',
            password='test_password',
        )
        # 認証用のトークンを作成
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={
                'email': 'test_email@example.com',
                'password': 'test_password',
            },
            format='json'
        )
        self.token = response.data.get('access')
        if self.token is None:
            raise ValueError('token is None')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)
        self.url = reverse('training-group-list')

    def test_list(self):
        # 全てのTrainingGroupを取得
        response = self.client.get(self.url)
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

    def test_update(self):
        # TrainingGroupを更新
        url = reverse('training-group-detail', args=[self.group.pk])
        response = self.client.patch(url, data={'name': 'test_group2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.group.refresh_from_db()
        self.assertEqual(self.group.name, 'test_group2')

    def test_destroy(self):
        # TrainingGroupを削除
        url = reverse('training-group-detail', args=[self.group.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TrainingGroup.objects.count(), 0)
