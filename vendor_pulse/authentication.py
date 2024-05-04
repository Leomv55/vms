from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    '''
        Custom Token Authentication class is to override the keyword used in the
        Authorization header to work with swagger UI.
        ref: https://github.com/tfranzel/drf-spectacular/issues/205
    '''
    keyword = "Bearer"
