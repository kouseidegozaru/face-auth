from documentation.schemas.swagger_schema_update import SwaggerSchemaUpdater
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from recognizer.serializers.recognize_serializers import TrainSerializer, PredictSerializer
from recognizer.views.recognize_views import TrainView, PredictView


# warning: モンキーパッチでviewのメソッドを上書きする
class Train(SwaggerSchemaUpdater):

    def run():
        """swaggerに追加する情報を記述する"""

        # TrainView.post
        TrainView.post = swagger_auto_schema(
            operation_summary="指定のgroupのTrainingDataを学習",
            operation_description="指定のgroupのTrainingDataを学習します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),
                               openapi.Parameter('X-CSRFToken', openapi.IN_HEADER, description="csrfトークン", type=openapi.TYPE_STRING),
                               openapi.Parameter('csrftoken', 'cookie', description="csrfトークン", type=openapi.TYPE_STRING),],
            responses={200: openapi.Response('成功'),
                       400: openapi.Response('シリアライザーエラーまたは学習エラー'),
                       403: openapi.Response('未認証のユーザー'),
                       404: openapi.Response('groupが見つからない'),
                       412: openapi.Response('TrainingDataの数が2つより少ない'),
                       },
        )(TrainView.post)


class Predict(SwaggerSchemaUpdater):

    def run():
        """swaggerに追加する情報を記述する"""

        # PredictView.post
        PredictView.post = swagger_auto_schema(
            operation_summary="指定のgroupの特徴モデルから推論",
            operation_description="指定のgroupの特徴モデルから推論します。",
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="認証トークン", type=openapi.TYPE_STRING),
                               openapi.Parameter('X-CSRFToken', openapi.IN_HEADER, description="csrfトークン", type=openapi.TYPE_STRING),
                               openapi.Parameter('csrftoken', 'cookie', description="csrfトークン", type=openapi.TYPE_STRING),],
            request_body=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY),
                    }
                ),
            responses={201: openapi.Response('成功'),
                       400: openapi.Response('シリアライザーエラーまたは推論エラーまたは画像に顔が存在しない'),
                       403: openapi.Response('未認証のユーザー'),
                       404: openapi.Response('groupが見つからない'),
                       412: openapi.Response('特徴モデルが存在しない'),
                       },
        )(PredictView.post)
