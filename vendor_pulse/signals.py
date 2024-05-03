from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Vendor


@receiver(pre_save, sender=Vendor)
def create_performance_history(sender, instance: Vendor, **kwargs):
    if instance.pk is None:
        return

    update_fields = kwargs.get("update_fields", [])
    should_create_historical_performance = (
        "on_time_delivery_rate" in update_fields or
        "quality_rating_avg" in update_fields or
        "average_response_time" in update_fields or
        "fulfillment_rate" in update_fields
    )
    if not should_create_historical_performance:
        return

    instance.create_historical_performance()
