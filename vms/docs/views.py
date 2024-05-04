from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView


@extend_schema(tags=["Schema"], summary="OpenAPI schema")
class OASView(SpectacularAPIView):
    pass
