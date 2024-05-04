from drf_spectacular.utils import extend_schema

from rest_framework.authtoken.views import ObtainAuthToken


@extend_schema(
    tags=["Authentication"],
    summary="Create token",
    description="Token based authentication is used to authenticate the user."
)
class CreateAPIAuthToken(ObtainAuthToken):
    pass
