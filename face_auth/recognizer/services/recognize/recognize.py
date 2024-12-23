import numpy as np
from sklearn.neighbors import NearestNeighbors
import face_recognition

from recognizer.services.recognize.types import LearningDataSet
from recognizer.services.tools.image_operations import open_image
from recognizer.services.recognize.feature_models import FeatureModel, PredictResult


def train_feature(data_set: LearningDataSet) -> FeatureModel:
    """学習を実行する

    Args:
        data_set (LearningDataSet): 学習に必要なデータのリスト

    Returns:
        FeatureModel: 学習後の特徴モデル
    """
    
    # ラベルの取得
    labels = list(map(lambda x: x.label, data_set.data))

    # 特徴量抽出
    image_paths = map(lambda x: x.image_path, data_set.data)
    images = map(lambda x: open_image(x), image_paths)
    face_images = map(detect_face, images)
    face_features = list(map(extract_face_feature, face_images))

    # 特徴量が取得できなかった場合のエラーチェック
    if any(feature is None for feature in face_features):
        raise ValueError("Error: Failed to extract face features from one or more images")

    # 学習
    model = NearestNeighbors(n_neighbors=1)
    model.fit(face_features)

    # 学習後の特徴モデルを返す
    return FeatureModel(model, labels)


def detect_face(image: np.ndarray) -> np.ndarray:
    """
    入力画像から顔領域を検出し、その領域を切り出して返す

    Args:
        image (np.ndarray): 入力画像

    Returns:
        np.ndarray: 顔領域が含まれる画像、もしくはNone
    """
    # 画像の有無
    if image is None:
        raise ValueError("Error: Image is None")
    
    # 顔領域を検出
    face_locations = face_recognition.face_locations(image)
    
    # 検出された顔領域の中から、最大の領域を取得
    if len(face_locations) > 0:
        top, right, bottom, left = max(face_locations, key=lambda r: (r[2]-r[0])*(r[1]-r[3]))
        face_image = image[top:bottom, left:right]
        return np.array(face_image)  # numpy配列として返す
    else:
        return None
    

def extract_face_feature(face_image: np.ndarray) -> np.ndarray:
    """
    入力された顔領域画像から特徴量を抽出して返す

    Args:
        face_image (np.ndarray): 顔領域を含む画像

    Returns:
        np.ndarray: 顔の特徴ベクトル、もしくはNone
    """
    # 画像の有無
    if face_image is None:
        raise ValueError("Error: FaceImage is None")
    
    # 顔画像から128次元の特徴ベクトルを抽出
    face_encoding = face_recognition.face_encodings(face_image)
    
    if len(face_encoding) > 0:
        # 最初の顔の特徴ベクトルを返す
        return face_encoding[0]
    else:
        return None


def predict_feature(feature_model: FeatureModel, face_image: np.ndarray) -> PredictResult:
    """
    入力された特徴モデルと顔画像から、顔画像に対する顔特徴を推定して返す

    Args:
        feature_model (FeatureModel): 特徴モデル
        face_image (np.ndarray): 顔画像

    Returns:
        str: 顔画像に対する顔特徴
    """
    face_feature = extract_face_feature(face_image)
    return feature_model.predict(face_feature)
