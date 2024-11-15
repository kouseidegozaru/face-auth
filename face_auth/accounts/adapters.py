from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        # メールアドレス確認メールに添付するurlの変更
        return 'https://testurl.com/verify-email/{key}'.format(key=emailconfirmation.key)