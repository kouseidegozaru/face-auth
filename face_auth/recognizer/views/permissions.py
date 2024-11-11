from rest_framework import permissions
from recognizer.models import TrainingGroup, TrainingData

class IsGroupOwnerOnly(permissions.BasePermission):
    """
    リクエストのpkから取得したグループの所有者のみ
    アクセスを許可するパーミッション
    """
    def has_permission(self, request, view):
        # URLからpkを取得
        pk = view.kwargs.get('pk')

        # pkが指定されていない場合はTrue
        if pk is None:
            return True

        try:
            # pkに基づいてオブジェクトを取得
            group = TrainingGroup.objects.get(pk=pk)
        except TrainingGroup.DoesNotExist:
            # オブジェクトが存在しない場合はアクセスを拒否
            return False

        # リクエストユーザーがオブジェクトの作成者であれば許可
        return group.owner == request.user
