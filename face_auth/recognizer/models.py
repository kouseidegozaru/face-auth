from django.db import models
import uuid
from accounts.models import User

class TrainingGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='名前', max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)


# 画像ファイルの保存先
def get_upload_to(self, filename):
    return f'recognizer/{self.group.id}/{filename}'
    
class TrainingData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='画像', upload_to=get_upload_to)
    label = models.CharField(verbose_name='ラベル', max_length=100)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)


# 特徴量ファイルの保存先
def get_feature_upload_to(self, filename):
    return f'feature/{self.group.user.id}/{filename}'

class FeatureFiles(models.Model):
    group = models.OneToOneField(TrainingGroup, on_delete=models.CASCADE)
    feature = models.FileField(verbose_name='特徴量ファイル', upload_to=get_feature_upload_to)
    labels = models.FileField(verbose_name='ラベルファイル', upload_to=get_feature_upload_to)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
