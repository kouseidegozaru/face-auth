from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import TrainingGroup, TrainingData
from ..serializers.models_serializers import TrainingGroupSerializer, TrainingDataSerializer
from ..services.validations import is_exist_face
from ..services.tools import open_image

class TrainingGroupViewSet(viewsets.ViewSet):
    # 認証済みのユーザーのみアクセス可能
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        現在のユーザーがオーナーのTrainingGroupをリストとして返す
        """
        queryset = TrainingGroup.objects.filter(owner=self.request.user)
        serializer = TrainingGroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        特定のTrainingGroupのTrainingDataを取得
        グループのオーナーが現在のユーザーでない場合は404エラー
        """
        try:
            instance = TrainingData.objects.get(group__id=pk, group__owner=self.request.user)
            serializer = TrainingDataSerializer(instance)
            return Response(serializer.data)
        except TrainingData.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        """
        新しいTrainingGroupを作成し、オーナーを現在のユーザーに設定
        """
        serializer = TrainingGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)  # オーナーを設定して保存
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        TrainingGroupの更新処理
        PATCHメソッドの場合は部分更新
        """
        partial = request.method == 'PATCH'
        instance = self.get_object(pk)

        # 現在のユーザーがオーナーでない場合、403エラー
        if instance.owner != request.user:
            return Response({"detail": "You do not have permission to edit this group."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TrainingGroupSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        TrainingGroupの削除処理
        現在のユーザーがオーナーでない場合、403エラー
        """
        instance = self.get_object(pk)
        if instance.owner != request.user:
            return Response({"detail": "You do not have permission to delete this group."}, status=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        """
        特定のTrainingGroupを取得
        存在しない場合やオーナーが異なる場合は404エラー
        """
        try:
            return TrainingGroup.objects.get(pk=pk, owner=self.request.user)
        except TrainingGroup.DoesNotExist:
            raise Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


class TrainingDataViewSet(viewsets.ViewSet):
    # 認証済みのユーザーのみアクセス可能
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        listメソッドはサポートされないため405エラーを返す
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        """
        特定のTrainingDataを取得
        グループのオーナーが現在のユーザーでない場合は404エラー
        """
        try:
            instance = TrainingData.objects.get(id=pk, group__owner=self.request.user)
            serializer = TrainingDataSerializer(instance)
            return Response(serializer.data)
        except TrainingData.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request,group_pk=None):
        """
        新しいTrainingDataを作成
        グループのオーナーが現在のユーザーでない場合は403エラー
        """
        serializer = TrainingDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # グループのオーナーが現在のユーザーか確認
        group = TrainingGroup.objects.get(pk=group_pk)
        if group.owner != request.user:
            return Response({"detail": "You do not have permission to create training data for this group."}, status=status.HTTP_403_FORBIDDEN)

        # 顔を検出していない場合は404エラー
        if not is_exist_face(open_image(request.data['image'])):
            return Response({"detail": "Face not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        TrainingDataの更新処理
        PATCHメソッドの場合は部分更新
        """
        partial = request.method == 'PATCH'
        instance = self.get_object(pk)

        # グループのオーナーが現在のユーザーでない場合は403エラー
        if instance.group.owner != request.user:
            return Response({"detail": "You do not have permission to edit this training data."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TrainingDataSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # 顔を検出していない場合は404エラー
        if not is_exist_face(open_image(instance.image)):
            return Response({"detail": "Face not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        TrainingDataの削除処理
        グループのオーナーが現在のユーザーでない場合は403エラー
        """
        instance = self.get_object(pk)
        if instance.group.owner != request.user:
            return Response({"detail": "You do not have permission to delete this training data."}, status=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        """
        特定のTrainingDataを取得
        存在しない場合やオーナーが異なる場合は404エラー
        """
        try:
            return TrainingData.objects.get(pk=pk, group__owner=self.request.user)
        except TrainingData.DoesNotExist:
            raise Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
