from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from .models import (
    Vendor,
    PurchaseOrder,
)


@receiver(pre_save, sender=Vendor)
def create_performance_history(sender, instance: Vendor, **kwargs):
    if instance.pk is None:
        return

    update_fields = kwargs.get("update_fields", [])
    if not update_fields:
        return

    should_create_historical_performance = (
        "on_time_delivery_rate" in update_fields or
        "quality_rating_avg" in update_fields or
        "average_response_time" in update_fields or
        "fulfillment_rate" in update_fields
    )
    if not should_create_historical_performance:
        return

    instance.create_historical_performance()


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics(sender, instance: PurchaseOrder, created, **kwargs):
    if not created:
        return

    vendor = instance.vendor
    update_fields = kwargs.get("update_fields", [])
    if not update_fields:
        return

    should_update_on_time_delivery_rate = "status" in update_fields and instance.status == PurchaseOrder.COMPLETED
    should_quality_rating_avg = "quality_rating" in update_fields
    should_update_average_response_time = "acknowledgment_date" in update_fields
    should_update_fulfillment_rate = "status" in update_fields

    if should_update_on_time_delivery_rate:
        vendor.update_on_time_delivery_rate()

    if should_quality_rating_avg:
        vendor.update_quality_rating_avg()

    if should_update_average_response_time:
        vendor.update_average_response_time()

    if should_update_fulfillment_rate:
        vendor.update_fulfillment_rate()
