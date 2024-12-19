from django.urls import reverse


class AuthTestMixin(object):
    def set_auth_token(self, user, password=None):
        # 認証トークンの取得
        response = self.client.post(
            reverse('custom_login'),
            {'email': user.email, 'password': password},
            format='json'
        )
        self.token = response.data.get("key")
        if not self.token:
            raise ValueError('Token retrieval failed')
        # 認証ヘッダーの設定
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token, **self.client._credentials)

class CsrfTestMixin(object):
    def set_csrf_token(self):
        # CSRFトークンの取得
        response = self.client.get(
            reverse('csrf_token'),
            format='json'
        )
        self.csrf_token = response.json().get("csrfToken")
        if not self.csrf_token:
            raise ValueError('CSRF token retrieval failed')
        # ヘッダーにCSRFトークンの設定
        self.client.credentials(HTTP_X_CSRFTOKEN=self.csrf_token, **self.client._credentials)
        # クッキーにCSRFトークンを設定
        self.client.cookies['csrftoken'] = self.csrf_token
