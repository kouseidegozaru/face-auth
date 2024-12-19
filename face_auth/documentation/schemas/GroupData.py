from documentation.schemas.swagger_schema_update import SwaggerSchemaUpdater
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from recognizer.serializers.models_serializers import TrainingDataSerializer
from recognizer.views.models_views import GroupDataViewSet


# warning: モンキーパッチでviewのメソッドを上書きする
class TrainingData(SwaggerSchemaUpdater):

    def run():
        """swaggerに追加する情報を記述する"""

        # GroupDataViewSet.list_images
        GroupDataViewSet.list_images = swagger_auto_schema(
            operation_summary="指定のgroupのTrainingDataの一覧を取得",
            operation_description="現在のユーザーのTrainingData一覧を取得します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),],
            responses={200: openapi.Response(schema=TrainingDataSerializer(many=True), description='成功'), 
                       404: openapi.Response('groupが見つからない')},
        )(GroupDataViewSet.list_images)

        # TrainingGroupViewSet.create_image
        GroupDataViewSet.create_image = swagger_auto_schema(
            operation_summary="指定のgroupにTrainingDataを作成",
            operation_description="指定のgroupにTrainingDataを作成します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),
                               openapi.Parameter('X-CSRFToken', openapi.IN_HEADER, description="csrfトークン", type=openapi.TYPE_STRING),],
            request_body=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY),
                        'label': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            responses={201: openapi.Response('成功'),
                       400: openapi.Response('シリアライザーエラーまたは画像に顔が存在しない'),
                       403: openapi.Response('未認証のユーザー'),
                       404: openapi.Response('groupが見つからない')
                       },
        )(GroupDataViewSet.create_image)