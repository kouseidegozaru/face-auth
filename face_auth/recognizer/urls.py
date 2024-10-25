from django.urls import path
from .views.data_requests import TrainingGroupViewSet, TrainingDataViewSet
from .views.data_train import TrainView, PredictView

training_group_list = TrainingGroupViewSet.as_view({
    'get': 'list',      # GET: /training-groups/ - TrainingGroup一覧
    'post': 'create',   # POST: /training-groups/ - TrainingGroup作成
})

training_group_detail = TrainingGroupViewSet.as_view({
    'get': 'retrieve',   # GET: /training-groups/<uuid:pk>/ - 特定のTrainingGroupのTrainingData一覧
    'patch': 'update',   # PATCH: /training-groups/<uuid:pk>/ - TrainingGroup更新
    'delete': 'destroy', # DELETE: /training-groups/<uuid:pk>/ - TrainingGroup削除
})

training_data_detail = TrainingDataViewSet.as_view({
    'get': 'retrieve',   # GET: /training-data/<uuid:pk>/ - 特定のTrainingData
    'patch': 'update',   # PATCH: /training-data/<uuid:pk>/ - TrainingData更新
    'delete': 'destroy', # DELETE: /training-data/<uuid:pk>/ - TrainingData削除
})

training_data_create = TrainingDataViewSet.as_view({
    'post': 'create',    # POST: /training-data/<uuid:group_pk>/ - TrainingData作成
})

urlpatterns = [
    path('training-groups/', training_group_list, name='training-group-list'),                  # GET, POST
    path('training-groups/<uuid:pk>/', training_group_detail, name='training-group-detail'),    # GET, PATCH, DELETE
    path('training-data/<uuid:pk>/', training_data_detail, name='training-data-detail'),        # GET, PATCH, DELETE
    path('training-data/<uuid:group_pk>/', training_data_create, name='training-data-create'),  # POST
    path('train/<uuid:pk>/', TrainView.as_view(), name='train'),
    path('predict/<uuid:pk>/', PredictView.as_view(), name='predict'),                          # POST
]
