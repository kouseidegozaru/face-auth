from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import uuid
from accounts.models import User
import os

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

@receiver(post_delete, sender=TrainingData)
def delete_image(sender, instance, **kwargs):
    # 画像ファイルを削除
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=TrainingData)
def update_image(sender, instance, **kwargs):
    # 画像ファイル名を更新する際に古い画像ファイルを削除
    if not instance.pk:
        return  # 新規インスタンスなら処理しない

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if old_instance.image and old_instance.image != instance.image:
        if os.path.isfile(old_instance.image.path):
            os.remove(old_instance.image.path)


class FeatureData(models.Model):
    group = models.OneToOneField(TrainingGroup, on_delete=models.CASCADE)
    feature = models.BinaryField(verbose_name='特徴量')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
