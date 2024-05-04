from rest_framework import serializers

from .models import (
    Vendor,
    PurchaseOrder,
)


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "vendor_code",
            "name",
            "contact_details",
            "address"
        )


class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor_code = serializers.ReadOnlyField(source="vendor.vendor_code")

    class Meta:
        model = PurchaseOrder
        exclude = ("id", )


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate"
        )
