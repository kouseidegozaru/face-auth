from documentation.schemas.swagger_schema_update import SwaggerSchemaUpdater
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from recognizer.serializers.models_serializers import TrainingDataSerializer
from recognizer.views.models_views import TrainingDataViewSet


# warning: モンキーパッチでviewのメソッドを上書きする
class TrainingData(SwaggerSchemaUpdater):

    def run():
        """swaggerに追加する情報を記述する"""

        # TrainingDataViewSet.list
        TrainingDataViewSet.list = swagger_auto_schema(
            operation_summary="TrainingDataの一覧を取得",
            operation_description="現在のユーザーのTrainingData一覧を取得します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),],
            responses={200: openapi.Response(schema=TrainingDataSerializer(many=True), description='成功'), 
                       404: openapi.Response('Not Found')},
        )(TrainingDataViewSet.list)

        # TrainingDataViewSet.retrieve
        TrainingDataViewSet.retrieve = swagger_auto_schema(
            operation_summary="特定のTrainingDataを取得",
            operation_description="特定のTrainingDataを取得します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),],
            responses={200: openapi.Response(schema=TrainingDataSerializer(), description='成功'), 
                       403: openapi.Response('未認証のユーザー'),
                       404: openapi.Response('training dataが見つからない')
                       },
        )(TrainingDataViewSet.retrieve)

        # TrainingDataViewSet.update
        TrainingDataViewSet.update = swagger_auto_schema(
            operation_summary="特定のTrainingDataを更新",
            operation_description="特定のTrainingDataを更新します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),
                               openapi.Parameter('X-CSRFToken', openapi.IN_HEADER, description="csrfトークン", type=openapi.TYPE_STRING),],
            request_body=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY),
                        'label': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            responses={200: openapi.Response(schema=TrainingDataSerializer(), description='成功'),
                       400: openapi.Response('シリアライザーエラー'),
                       403: openapi.Response('未認証のユーザー'),
                       404: openapi.Response('training dataが見つからない')},
        )(TrainingDataViewSet.update)

        # TrainingDataViewSet.destroy
        TrainingDataViewSet.destroy = swagger_auto_schema(
            operation_summary="特定のTrainingDataを削除",
            operation_description="特定のTrainingDataを削除します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),
                               openapi.Parameter('X-CSRFToken', openapi.IN_HEADER, description="csrfトークン", type=openapi.TYPE_STRING),],
            responses={204: openapi.Response('成功'),
                       400: openapi.Response('シリアライザーエラー'),
                       403: openapi.Response('未認証のユーザー'),
                       404: openapi.Response('training dataが見つからない')},
        )(TrainingDataViewSet.destroy)
