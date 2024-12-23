from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_custom_password_reset_confirm_url():
    return settings.ACCOUNT_PASSWORD_RESET_CONFIRM_URL