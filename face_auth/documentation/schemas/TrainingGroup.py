from recognizer.views.models_views import TrainingGroupViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# warning: モンキーパッチでviewのメソッドを上書きする

def update_swagger():
    # TrainingGroupViewSet.list
    TrainingGroupViewSet.list = swagger_auto_schema(
        operation_summary="TrainingGroupの一覧を取得",
        operation_description="現在のユーザーのTrainingGroup一覧を取得します。",
        responses={200: openapi.Response('成功'), 404: openapi.Response('Not Found')},
    )(TrainingGroupViewSet.list)

    # TrainingGroupViewSet.retrieve
    TrainingGroupViewSet.retrieve = swagger_auto_schema(
        operation_summary="特定のTrainingGroupを取得",
        operation_description="特定のTrainingGroupを取得します。",
        responses={200: openapi.Response('成功'), 404: openapi.Response('Not Found')},
    )(TrainingGroupViewSet.retrieve)
