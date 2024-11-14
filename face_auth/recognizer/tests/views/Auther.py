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
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
