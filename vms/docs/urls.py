from django.urls import path
from django.conf import settings

from drf_spectacular.views import (
    SpectacularRedocView,
    SpectacularSwaggerView
)

from .views import OASView


urlpatterns = [
    path(
        "schema/", OASView.as_view(custom_settings=settings.SPECTACULAR_SETTINGS), name="schema"
    ),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path(
        "", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
