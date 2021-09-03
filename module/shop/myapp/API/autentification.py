from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TemporaryTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key=key)
        if (timezone.now() - token.created).seconds > settings.TOKEN_TTL:
            token.delete()
            raise exceptions.AuthenticationFailed(_('Token expired'))
        return user, token
