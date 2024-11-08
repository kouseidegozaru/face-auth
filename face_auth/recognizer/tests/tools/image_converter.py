from recognizer.services.tools.image_operations import open_image
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
import numpy as np

def SimpleUploadedFile_to_image(SimpleUploadedFile : SimpleUploadedFile) -> np.ndarray:
    """
    SimpleUploadedFileをnumpy配列の画像に変換する
    """
    byte_image = BytesIO(SimpleUploadedFile.read())
    return open_image(byte_image)
