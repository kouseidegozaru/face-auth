import numpy as np
import PIL.Image as Image
from io import BytesIO

def get_test_image() -> np.ndarray:
    """
    テスト用の画像データを返す
    """
    image = Image.new("RGB", (100, 100), color=(0, 0, 0))
    return np.array(image)

def get_test_image_as_bytes() -> bytes:
    """
    テスト用の画像データをbytes型で返す
    """
    image = Image.new("RGB", (100, 100), color=(0, 0, 0))
    buf = BytesIO()
    image.save(buf, format='JPEG')

    return buf.getvalue()
