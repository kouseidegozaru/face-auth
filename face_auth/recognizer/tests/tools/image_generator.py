from io import BytesIO

import PIL.Image as Image
from django.core.files.uploadedfile import SimpleUploadedFile


def test_image() -> Image:
    return Image.new("RGB", (100, 100), color=(0, 0, 0))

def test_image_as_bytes() -> bytes:
    """
    テスト用の画像データをbytes型で返す
    """
    image = test_image()
    buf = BytesIO()
    image.save(buf, format='JPEG')

    return buf.getvalue()

def SimpleUploadedImage(name='test_image.jpg', 
                        data=test_image_as_bytes(), 
                        content_type='image/jpeg'
                        ) -> SimpleUploadedFile:
    """
    テスト用の画像データをSimpleUploadedFile型で返す
    """
    return SimpleUploadedFile(name, data, content_type=content_type)
