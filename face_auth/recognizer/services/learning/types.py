from typing import Generator

# 学習に必要なデータのレコードの型
class LearningDataRecordType():
    def __init__(self, label: str, image_path: str):
        self._label = label
        self._image_path = image_path

    def image_path(self) -> str:
        return self._image_path
    
    def label(self) -> str:
        return self._label

# 学習に必要なデータのリスト
class LearningDataSet():
    def __init__(self):
        self.data = []

    def add(self, label: str, image_path: str):
        self.data.append(LearningDataRecordType(label, image_path))

    def data(self) -> Generator[LearningDataRecordType, None, None]:
        yield from self.data
