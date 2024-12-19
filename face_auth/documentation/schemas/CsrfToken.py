from documentation.schemas.swagger_schema_update import SwaggerSchemaUpdater
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from accounts.views import CsrfTokenView


# warning: モンキーパッチでviewのメソッドを上書きする
class CsrfToken(SwaggerSchemaUpdater):

    def run():
        """swaggerに追加する情報を記述する"""

        # CsrfTokenView.get
        CsrfTokenView.get = swagger_auto_schema(
            operation_summary="csrfトークンを発行します",
            operation_description="csrfトークンを発行します。",
            manual_parameters=[],
            responses={200: openapi.Response(schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'csrfToken': openapi.Schema(type=openapi.TYPE_STRING)}), description='成功')},
        )(CsrfTokenView.get)
