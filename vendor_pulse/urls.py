from django.urls import path, include

from .routers import vp_api_router

urlpatterns = [
    path("", include(vp_api_router.urls)),
]
