from ...models import TrainingData, TrainingGroup
from .types import LearningDataSet

def create_training_data_set(group_id) -> LearningDataSet:
    """
    TrainingDataから
    学習に必要なデータセットを作成
    """

    # 学習対象のTrainingDataを取得
    training_group = TrainingGroup.objects.get(id=group_id)
    training_datas = TrainingData.objects.filter(group=training_group)

    # 学習に必要なデータセットを作成
    data_set = LearningDataSet()
    for training_data in training_datas:
        data_set.add(training_data.label, training_data.image.path)
    
    return data_set
    
    