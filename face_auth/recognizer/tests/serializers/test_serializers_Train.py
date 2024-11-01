from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.exceptions import ValidationError
from ...models import TrainingGroup, TrainingData
from ...serializers.recognize_serializers import TrainSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class TestTrainSerializer(TestCase):

    def setUp(self):
        # テストユーザーとトレーニンググループの設定
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )

        # トレーニンググループの作成
        self.group = TrainingGroup.objects.create(name="test_group", owner=self.user)
        
        # テスト用の画像データを2つ作成
        self.image1 = TrainingData.objects.create(
            group=self.group,
            image=SimpleUploadedFile("test_image1.jpg", b"test_image_data", content_type="image/jpeg"),
            label="label1"
        )
        self.image2 = TrainingData.objects.create(
            group=self.group,
            image=SimpleUploadedFile("test_image2.jpg", b"test_image_data", content_type="image/jpeg"),
            label="label2"
        )

        # 削除対象のファイルパスを保持するリスト
        self.image_paths = [self.image1.image.path, self.image2.image.path]

        # シリアライザーで使用するAPIリクエストの設定
        self.factory = APIRequestFactory()
        self.url = reverse('train-group', args=[self.group.pk])  # 適切なエンドポイントに合わせる

    def tearDown(self):
        # 画像ファイルを削除
        for image_path in self.image_paths:
            if image_path and os.path.exists(image_path):
                os.remove(image_path)

    def test_validate_success(self):
        # 正常なトレーニングシリアライザーの検証
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        serializer = TrainSerializer(data={"pk": self.group.pk}, context={"request": request})
        
        # シリアライザーが正常に検証されることを確認
        self.assertTrue(serializer.is_valid())

    def test_validate_fail_insufficient_images(self):
        # トレーニンググループに画像が1つしかない場合の検証
        # 最初に画像の1つを削除して2枚未満にする
        self.image2.delete()

        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        serializer = TrainSerializer(data={"pk": self.group.pk}, context={"request": request})

        with self.assertRaises(ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        
        # エラーメッセージの確認
        self.assertIn("You must upload at least two images to train this group.", str(e.exception))
