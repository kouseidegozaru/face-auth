import numpy as np
import PIL.Image as Image

def get_test_image() -> np.ndarray:
    """
    テスト用の画像データを返す
    """
    image = Image.new("RGB", (100, 100), color=(0, 0, 0))
    return np.array(image)
