from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.openapi import OpenApiTypes, OpenApiParameter

from .serializers import (
    VendorPerformanceSerializer,
    PurchaseOrderSerializer,
)


class PurchaseOrderSchema:
    @classmethod
    def schema(cls):
        return extend_schema(tags=["Purchase orders"])

    @classmethod
    def docs(cls):
        return extend_schema_view(
            list=cls.list_purchase_orders(),
            create=cls.create_purchase_order(),
            retrieve=cls.retrieve_purchase_order(),
            update=cls.update_purchase_order(),
            partial_update=cls.partial_update_purchase_order(),
            destroy=cls.destroy_purchase_order(),
            acknowledge=cls.acknowledge_purchase_order(),
        )

    @classmethod
    def list_purchase_orders(cls):
        return extend_schema(
            summary="List purchase orders",
            description="Get a list of purchase orders."
        )

    @classmethod
    def create_purchase_order(cls):
        return extend_schema(
            summary="Create purchase order",
            description="Create a new purchase order."
        )

    @classmethod
    def retrieve_purchase_order(cls):
        return extend_schema(
            summary="Retrieve purchase order",
            description="Get a purchase order by ID."
        )

    @classmethod
    def update_purchase_order(cls):
        return extend_schema(
            summary="Update purchase order",
            description="Update a purchase order by ID."
        )

    @classmethod
    def partial_update_purchase_order(cls):
        return extend_schema(
            summary="Partial update purchase order",
            description="Partially update a purchase order by ID."
        )

    @classmethod
    def destroy_purchase_order(cls):
        return extend_schema(
            summary="Delete purchase order",
            description="Delete a purchase order by ID."
        )

    @classmethod
    def acknowledge_purchase_order(cls):
        return extend_schema(
            summary="Acknowledge purchase order",
            description="Acknowledge a purchase order by ID.",
            responses=PurchaseOrderSerializer
        )


class VendorSchema:
    @classmethod
    def schema(cls):
        return extend_schema(tags=["Vendors"])

    @classmethod
    def docs(cls):
        return extend_schema_view(
            list=cls.list_vendors(),
            create=cls.create_vendor(),
            retrieve=cls.retrieve_vendor(),
            update=cls.update_vendor(),
            partial_update=cls.partial_update_vendor(),
            destroy=cls.destroy_vendor(),
            performance=cls.vendor_performance(),
        )

    @classmethod
    def list_vendors(cls):
        return extend_schema(
            summary="List vendors",
            description="Get a list of vendors."
        )

    @classmethod
    def create_vendor(cls):
        return extend_schema(
            summary="Create vendor",
            description="Create a new vendor."
        )

    @classmethod
    def retrieve_vendor(cls):
        return extend_schema(
            summary="Retrieve vendor",
            description="Get a vendor by ID."
        )

    @classmethod
    def update_vendor(cls):
        return extend_schema(
            summary="Update vendor",
            description="Update a vendor by ID."
        )

    @classmethod
    def partial_update_vendor(cls):
        return extend_schema(
            summary="Partial update vendor",
            description="Partially update a vendor by ID."
        )

    @classmethod
    def destroy_vendor(cls):
        return extend_schema(
            summary="Delete vendor",
            description="Delete a vendor by ID."
        )

    @classmethod
    def vendor_performance(cls):
        return extend_schema(
            summary="Vendor performance",
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
