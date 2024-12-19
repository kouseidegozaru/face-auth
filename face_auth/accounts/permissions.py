from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class PostHasCsrfTokenNonGetMethod(permissions.BasePermission):
    """
    GETメソッド以外の
    リクエストのヘッダーとcookieに設定されている
    CSRFトークンを検証する
    """
    def has_permission(self, request, view):
        try:
            if request.method != 'GET':
                # CSRFトークンを検証
                csrf_token_from_cookie = request.COOKIES.get('csrftoken', None)
                csrf_token_from_header = request.headers.get('X-CSRFToken', None)
                if csrf_token_from_cookie and csrf_token_from_header and csrf_token_from_cookie == csrf_token_from_header:
                    return True
            else:
                return True
        except:
            # CSRFトークンが無効の場合は拒否
            raise PermissionDenied(request.method)
    