from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        # メールアドレス確認メールに添付するurlの変更
        if settings.DEBUG:
            # デバッグ時はデフォルトのメールアドレス確認url
            return super().get_email_confirmation_url(request, emailconfirmation)
        else:
            # メールアドレス確認メールに添付するurl
            return settings.ACCOUNT_EMAIL_CONFIRMATION_URL.format(key=emailconfirmation.key)