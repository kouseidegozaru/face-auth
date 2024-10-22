from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import TrainingGroup
from .logic import feature_training

class Train(APIView):
    # 認証済みのユーザーのみアクセス可能
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        group = get_object_or_404(TrainingGroup, pk=pk)

        # オーナーの確認
        if group.owner != request.user:
            return Response({"detail": "You do not have permission to train this group."}, status=status.HTTP_403_FORBIDDEN)

        # 学習
        feature_training(group.id)
        
        return Response(status=status.HTTP_200_OK)
