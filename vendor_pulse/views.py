
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import (
    Vendor,
    PurchaseOrder,
)
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
)
from .authentication import CustomTokenAuthentication


class VendorModelViewSet(ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderModelViewSet(ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
