from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import Token


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()
        if not auth or auth[0].lower() != 'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = Token.objects.get(key=auth[1])
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such token.')

        return token.user, token
