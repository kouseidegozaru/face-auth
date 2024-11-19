from documentation.schemas.swagger_schema_update import SwaggerSchemaUpdater
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from recognizer.serializers.models_serializers import TrainingGroupSerializer
from recognizer.views.models_views import TrainingGroupViewSet


# warning: モンキーパッチでviewのメソッドを上書きする
class TrainingGroup(SwaggerSchemaUpdater):

    def run():
        """swaggerに追加する情報を記述する"""

        # TrainingGroupViewSet.list
        TrainingGroupViewSet.list = swagger_auto_schema(
            operation_summary="TrainingGroupの一覧を取得",
            operation_description="現在のユーザーのTrainingGroup一覧を取得します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),],
            responses={200: openapi.Response(schema=TrainingGroupSerializer(many=True), description='成功'), 
                       404: openapi.Response('Not Found')},
        )(TrainingGroupViewSet.list)

        # TrainingGroupViewSet.retrieve
        TrainingGroupViewSet.retrieve = swagger_auto_schema(
            operation_summary="特定のTrainingGroupを取得",
            operation_description="特定のTrainingGroupを取得します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),],
            responses={200: openapi.Response(schema=TrainingGroupSerializer(), description='成功'), 
                       403: openapi.Response('未認証のユーザー'),
                       404: openapi.Response('groupが見つからない')
                       },
        )(TrainingGroupViewSet.retrieve)

        # TrainingGroupViewSet.create
        TrainingGroupViewSet.create = swagger_auto_schema(
            operation_summary="TrainingGroupを作成",
            operation_description="TrainingGroupを作成します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),],
            request_body=TrainingGroupSerializer(),
            responses={201: openapi.Response('成功'),
                       400: openapi.Response('シリアライザーエラー'),
                       403: openapi.Response('未認証のユーザー'),
                       404: openapi.Response('groupが見つからない')
                       },
        )(TrainingGroupViewSet.create)

        # TrainingGroupViewSet.update
        TrainingGroupViewSet.update = swagger_auto_schema(
            operation_summary="特定のTrainingGroupを更新",
            operation_description="特定のTrainingGroupを更新します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),],
            request_body=TrainingGroupSerializer(),
            responses={200: openapi.Response(schema=TrainingGroupSerializer(), description='成功'),
                       400: openapi.Response('シリアライザーエラー'),
                       403: openapi.Response('未認証のユーザー'),
                       404: openapi.Response('groupが見つからない')},
        )(TrainingGroupViewSet.update)

        # TrainingGroupViewSet.destroy
        TrainingGroupViewSet.destroy = swagger_auto_schema(
            operation_summary="特定のTrainingGroupを削除",
            operation_description="特定のTrainingGroupを削除します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),],
            responses={204: openapi.Response('成功'),
                       400: openapi.Response('シリアライザーエラー'),
                       403: openapi.Response('未認証のユーザー'),
                       404: openapi.Response('groupが見つからない')},
        )(TrainingGroupViewSet.destroy)
