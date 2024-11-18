from documentation.schemas.swagger_schema_update import SwaggerSchemaUpdater
from django.conf import settings


def apply_monkey_patches():
    # warning: モンキーパッチでviewのメソッドを上書きする
    SwaggerSchemaUpdater.run_for_subclasses(settings.SWAGGER_SCHEMA_UPDATERS)
