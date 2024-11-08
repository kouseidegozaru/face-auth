from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from ..models import TrainingGroup, TrainingData
from ..serializers.models_serializers import TrainingGroupSerializer, TrainingDataSerializer
from django.shortcuts import get_object_or_404


class TrainingGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # すべてのグループを取得
    def list(self, request):
        groups = TrainingGroup.objects.filter(owner=request.user)
        serializer = TrainingGroupSerializer(groups, many=True)
        return Response(serializer.data)

    # 特定のグループを取得
    def retrieve(self, request, pk=None):
        group = get_object_or_404(TrainingGroup, pk=pk, owner=request.user)
        serializer = TrainingGroupSerializer(group)
        return Response(serializer.data)

    # 新しいグループを追加
    def create(self, request):
        serializer = TrainingGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # グループ名を変更（他の項目は変更不可）
    def update(self, request, pk=None):
        group = get_object_or_404(TrainingGroup, pk=pk, owner=request.user)
        serializer = TrainingGroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(TrainingGroupSerializer(group).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # グループを削除
    def destroy(self, request, pk=None):
        group = get_object_or_404(TrainingGroup, pk=pk, owner=request.user)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrainingDataViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # すべての画像データを取得
    def list(self, request):
        data = TrainingData.objects.filter(group__owner=request.user)
        serializer = TrainingDataSerializer(data, many=True)
        return Response(serializer.data)

    # 特定の画像データを取得
    def retrieve(self, request, pk=None):
        data = get_object_or_404(TrainingData, pk=pk, group__owner=request.user)
        serializer = TrainingDataSerializer(data)
        return Response(serializer.data)

    # 画像とラベル名を変更（他の項目は変更不可）
    def update(self, request, pk=None):
        data = get_object_or_404(TrainingData, pk=pk, group__owner=request.user)
        serializer = TrainingDataSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(TrainingDataSerializer(data).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 特定の画像を削除
    def destroy(self, request, pk=None):
        data = get_object_or_404(TrainingData, pk=pk, group__owner=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupDataViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # 特定のグループのすべての画像を取得
    @action(detail=True, methods=["get"], url_path="images")
    def list_images(self, request, group_pk=None):
        group = get_object_or_404(TrainingGroup, pk=group_pk, owner=request.user)
        images = TrainingData.objects.filter(group=group)
        serializer = TrainingDataSerializer(images, many=True)
        return Response(serializer.data)

    # 特定のグループに画像を追加
    @action(detail=True, methods=["post"], url_path="images")
    def create_image(self, request, group_pk=None):
        group = get_object_or_404(TrainingGroup, pk=group_pk, owner=request.user)
        serializer = TrainingDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
