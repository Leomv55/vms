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


@receiver(pre_save, sender=PurchaseOrder)
def save_updated_fields(sender, instance: PurchaseOrder, **kwargs):
    if instance.pk is None:
        return

    old_instance = PurchaseOrder.objects.get(pk=instance.pk)
    instance._status = old_instance.status
    instance._acknowledgment_date = old_instance.acknowledgment_date
    instance._quality_rating = old_instance.quality_rating


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics(sender, instance: PurchaseOrder, created, **kwargs):
    if created:
        return

    vendor = instance.vendor
    should_update_on_time_delivery_rate = instance._status != instance.status and instance.status == PurchaseOrder.COMPLETED
    should_quality_rating_avg = instance._quality_rating != instance.quality_rating
    should_update_average_response_time = instance._acknowledgment_date != instance.acknowledgment_date
    should_update_fulfillment_rate = instance._status != instance.status

    if should_update_on_time_delivery_rate:
        vendor.update_on_time_delivery_rate()

    if should_quality_rating_avg:
        vendor.update_quality_rating_avg()

    if should_update_average_response_time:
        vendor.update_average_response_time()

    if should_update_fulfillment_rate:
        vendor.update_fulfillment_rate()
