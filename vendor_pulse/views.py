from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

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
        parameters=[
            OpenApiParameter(
                name="recalculate",
                description='''Recalculate the performance metrics
                <ul>
                    <li>0 for not to recalculate. (Default)</li>
                    <li>1 to recalculate.</li>
                </ul>''',
                default="0",
                required=False,
                type=OpenApiTypes.NUMBER,
                enum=[0, 1],
            )
        ],
        responses=VendorPerformanceSerializer
    )
    @action(detail=True, methods=["get"])
    def performance(self, request, pk=None):
        vendor: Vendor = self.get_object()
        recalculate = request.query_params.get("recalculate", "0") == "1"
        if recalculate:
            vendor.recalculate_performance_metrics()
        vender_performance = VendorPerformanceSerializer(vendor)
        return Response(vender_performance.data)


class PurchaseOrderModelViewSet(ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    @extend_schema(
        description="Acknowledge the purchase order.",
        request=None,
        responses=PurchaseOrderSerializer
    )
    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        purchase_order: PurchaseOrder = self.get_object()
        purchase_order.acknowledge()
        purchase_order_serializer = PurchaseOrderSerializer(purchase_order)
        return Response(purchase_order_serializer.data)
