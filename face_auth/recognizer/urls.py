from django.urls import path
from recognizer.views.models_views import (GroupDataViewSet,
                                           TrainingDataViewSet,
                                           TrainingGroupViewSet)
from recognizer.views.recognize_views import PredictView, TrainView

training_group_list = TrainingGroupViewSet.as_view({
    'get': 'list',      # GET: /training-groups/ - TrainingGroup一覧
    'post': 'create',   # POST: /training-groups/ - TrainingGroup作成
})

training_group_detail = TrainingGroupViewSet.as_view({
    'get': 'retrieve',   # GET: /training-groups/<uuid:pk>/ - 特定のTrainingGroup取得
    'patch': 'update',   # PATCH: /training-groups/<uuid:pk>/ - TrainingGroup更新
    'delete': 'destroy', # DELETE: /training-groups/<uuid:pk>/ - TrainingGroup削除
})

training_data_list = TrainingDataViewSet.as_view({
    'get': 'list',      # GET: /training-data/ - TrainingData一覧
})

training_data_detail = TrainingDataViewSet.as_view({
    'get': 'retrieve',   # GET: /training-data/<uuid:pk>/ - 特定のTrainingData取得
    'patch': 'update',   # PATCH: /training-data/<uuid:pk>/ - TrainingData更新
    'delete': 'destroy', # DELETE: /training-data/<uuid:pk>/ - TrainingData削除
})

group_data_list_create = GroupDataViewSet.as_view({
    'get': 'list_images',   # GET: /training-groups/<uuid:group_pk>/images/ - グループごとの画像一覧
    'post': 'create_image', # POST: /training-groups/<uuid:group_pk>/images/ - グループに画像追加
})

urlpatterns = [
    path('training-groups/', training_group_list, name='training-group-list'),                   # GET, POST
    path('training-groups/<uuid:pk>/', training_group_detail, name='training-group-detail'),     # GET, PATCH, DELETE
    path('training-data/', training_data_list, name='training-data-list'),                       # GET
    path('training-data/<uuid:pk>/', training_data_detail, name='training-data-detail'),         # GET, PATCH, DELETE
    path('training-groups/<uuid:group_pk>/images/', group_data_list_create, name='group-data'),  # GET, POST for images in group
    path('train/<uuid:pk>/', TrainView.as_view(), name='train'),                                 # Train model
    path('predict/<uuid:pk>/', PredictView.as_view(), name='predict'),                           # Predict with model
]
