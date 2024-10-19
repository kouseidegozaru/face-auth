from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import TrainingGroup, TrainingData
from .serializers import TrainingGroupSerializer, TrainingDataSerializer


class TrainingGroupViewSet(viewsets.ModelViewSet):
    queryset = TrainingGroup.objects.all()
    serializer_class = TrainingGroupSerializer
    permission_classes = [IsAuthenticated]  # 認証済みのユーザーのみアクセス可能

    def get_queryset(self):
        # 現在のユーザーがオーナーのTrainingGroupのみを取得
        return TrainingGroup.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # 新しいTrainingGroupのオーナーを現在のユーザーに設定
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        # 部分更新を許可
        partial = request.method == 'PATCH'
        
        # 現在のユーザーがオーナーであることを確認
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({"detail": "You do not have permission to edit this group."}, status=status.HTTP_403_FORBIDDEN)
        
        # ownerの更新を防ぐために、オーバーライド
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # 現在のユーザーがオーナーであることを確認
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({"detail": "You do not have permission to delete this group."}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrainingDataViewSet(viewsets.ModelViewSet):
    queryset = TrainingData.objects.all()
    serializer_class = TrainingDataSerializer
    permission_classes = [IsAuthenticated]  # 認証済みのユーザーのみアクセス可能

    def get_queryset(self):
        # 現在のユーザーがオーナーのTrainingDataのみを取得
        return TrainingData.objects.filter(group__owner=self.request.user)
    
    def perform_create(self, serializer):
        # TrainingDataを作成する際に、グループのオーナーが現在のユーザーであることを確認
        group = serializer.validated_data.get('group')  # リクエストからグループを取得
        if group.owner != self.request.user:
            return Response({"detail": "You do not have permission to create training data for this group."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def update(self, request, *args, **kwargs):
        # 部分更新を許可
        partial = request.method == 'PATCH'
        
        # 現在のユーザーがオーナーであることを確認
        instance = self.get_object()
        if instance.group.owner != request.user:
            return Response({"detail": "You do not have permission to edit this training data."}, status=status.HTTP_403_FORBIDDEN)
        
        # groupの更新を防ぐために、オーバーライド
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # 現在のユーザーがオーナーであることを確認
        instance = self.get_object()
        if instance.group.owner != request.user:
            return Response({"detail": "You do not have permission to delete this training data."}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
