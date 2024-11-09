import os
from recognizer.models import TrainingData
from django.conf import settings

def clear_media():
    """
    mediaディレクトリのすべてのファイルとディレクトリを削除する
    """
    # メディアディレクトリのパスを取得
    media_dir = settings.MEDIA_ROOT
    # メディアディレクトリ内のすべてのファイルとディレクトリを削除
    for root, dirs, files in os.walk(media_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
