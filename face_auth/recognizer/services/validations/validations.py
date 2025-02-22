import numpy as np
from recognizer.services.recognize.recognize import detect_face,extract_face_feature


def is_exist_face(image : np.ndarray) -> bool:
    """
    入力された画像が顔画像の場合にTrueを返す
    """
    face_image = detect_face(image)
    if face_image is None:
        return False

    face_feature = extract_face_feature(face_image)
    if face_feature is None:
        return False
    
    return True