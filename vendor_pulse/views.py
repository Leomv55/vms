from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from .models import (
    Vendor,
    PurchaseOrder,
)
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    VendorPerformanceSerializer,
)
from .authentication import CustomTokenAuthentication


class VendorModelViewSet(ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @extend_schema(
        description="Get performance metrics for the vendor.",
        responses=VendorPerformanceSerializer
    )
    @action(detail=True, methods=["get"])
    def performance(self, request, pk=None):
        vendor: Vendor = self.get_object()
        vendor.recalculate_performance_metrics()
        vender_performance = VendorPerformanceSerializer(vendor)
        return Response(vender_performance.data)


class PurchaseOrderModelViewSet(ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
