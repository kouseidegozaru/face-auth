from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingGroupViewSet

# ルーターを作成
router = DefaultRouter()

router.register(r'training-groups', TrainingGroupViewSet, basename='traininggroup')
# GET: /training-groups/ ログイン済みユーザーのTrainingGroup一覧
# POST: /training-groups/ ログイン済みユーザーのTrainingGroup作成
# PATCH: /training-groups/<int:pk>/ ログイン済みユーザーのTrainingGroup更新
# DELETE: /training-groups/<int:pk>/ ログイン済みユーザーのTrainingGroup削除

urlpatterns = [
    path('', include(router.urls)),  # ルーターのURLを含める
]
