from recognizer.models import TrainingData
from django.db.models import Model


class ClearTestDataMixin:
    """
    テストデータをクリアするためのMixin
    wornings: 
        このクラスを多重継承する際は、TestCaseクラスよりも先に記述する
        (tearDownメソッドがTestCaseクラスの方に上書きされるのを防ぐため)
    usage:
        class TestView(ClearTestDataMixin, TestCase):
    """
    ClearObjects: list[type[Model]] = []

    def tearDown(self):
        super().tearDown()
        self.clear_test_data()

    def clear_test_data(self):
        for obj in self.ClearObjects:
            obj.objects.all().delete()


class ClearTrainingDataMixin(ClearTestDataMixin):
    """
    TrainingDataをクリアするためのMixin
    """
    ClearObjects = [TrainingData]
