from django.utils.translation import gettext_lazy as _

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', "")
        if not token:
            AuthenticationFailed(_('No token provided'))

        return self.authenticate_credentials(token)
