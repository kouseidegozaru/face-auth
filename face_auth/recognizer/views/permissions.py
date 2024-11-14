from recognizer.models import TrainingData, TrainingGroup
from rest_framework import permissions
from rest_framework.exceptions import NotFound


class IsGroupOwnerOnly(permissions.BasePermission):
    """
    リクエストのpkから取得したグループの所有者のみ
    アクセスを許可するパーミッション
    """
    def has_permission(self, request, view):
        # URLからpkまたはgroup_pkの存在する方を取得
        pk = view.kwargs.get('pk')
        group_pk = view.kwargs.get('group_pk')

        # group_pkを優先
        if group_pk is not None:
            pk = group_pk

        # pkが指定されていない場合はTrue
        if pk is None:
            return True

        try:
            # pkに基づいてオブジェクトを取得
            group = TrainingGroup.objects.get(pk=pk)
        except TrainingGroup.DoesNotExist:
            # オブジェクトが存在しない場合は404
            raise NotFound(detail="TrainingGroup does not exist.")

        # リクエストユーザーがオブジェクトの作成者であれば許可
        return group.owner == request.user


class IsGroupDataOwnerOnly(permissions.BasePermission):
    """
    リクエストのpkから取得したデータのグループの所有者のみ
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
            group = TrainingData.objects.get(pk=pk).group
        except TrainingData.DoesNotExist:
            # オブジェクトが存在しない場合は404
            raise NotFound(detail="TrainingData does not exist.")
        except TrainingGroup.DoesNotExist:
            # オブジェクトが存在しない場合は404
            raise NotFound(detail="TrainingGroup does not exist.")

        # リクエストユーザーがオブジェクトの作成者であれば許可
        return group.owner == request.user
