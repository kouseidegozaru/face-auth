import numpy as np
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def generate_random_image(filename="random_image.png") -> ContentFile:
    # ランダムな画像データを生成
    image_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    # numpy配列をPillowのImageオブジェクトに変換
    image = Image.fromarray(image_array)
    
    # BytesIOを使用して一時的に画像データを保存
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    
    # ContentFileとして画像を返す
    return ContentFile(buffer.read(), name=filename)
