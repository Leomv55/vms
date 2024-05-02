from rest_framework import routers

from .views import (
    VendorModelViewSet,
    PurchaseOrderModelViewSet,
)

vp_api_router = routers.DefaultRouter()
vp_api_router.register(r'vendors', VendorModelViewSet)
vp_api_router.register(r'purchase_orders', PurchaseOrderModelViewSet)
