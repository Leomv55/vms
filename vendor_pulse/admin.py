from django.contrib import admin

from .models import (
    Vendor,
    PurchaseOrder,
    HistoricalPerformance,
)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor_code", "on_time_delivery_rate", "quality_rating_avg", "average_response_time", "fulfillment_rate")


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("po_number", "vendor", "order_date", "delivery_date", "status", "quality_rating", "issue_date", "acknowledgment_date")
    list_filter = ("status", )


@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ("vendor", "date", "on_time_delivery_rate", "quality_rating_avg", "average_response_time", "fulfillment_rate")
