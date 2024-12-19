from face_auth.settings import *

INSTALLED_APPS += [
    'documentation',
    'drf_yasg',
]
# swaggerのスキーマ情報が記載されているモジュール
SWAGGER_SCHEMA_UPDATERS = [
    'documentation.schemas'
]
