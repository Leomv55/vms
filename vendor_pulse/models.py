from django.db import models
from django.db.models import Avg, F
from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.vendor_code

    def calculate_on_time_delivery_rate(self):
        current_time = timezone.now()
        completed_orders = self.purchase_orders.filter(
            status=PurchaseOrder.COMPLETED
        )
        completed_count = completed_orders.count()
        if completed_count == 0:
            return 0
        on_time_count = completed_orders.filter(
            delivery_date__lte=current_time
        ).count()
        return on_time_count / completed_count

    def update_on_time_delivery_rate(self):
        self.on_time_delivery_rate = self.calculate_on_time_delivery_rate()
        self.save(update_fields=["on_time_delivery_rate"])

    def calculate_quality_rating_avg(self):
        return self.purchase_orders.filter(
            status=PurchaseOrder.COMPLETED,
            quality_rating__isnull=False
        ).aggregate(Avg("quality_rating", default=0.0))["quality_rating__avg"]

    def update_quality_rating_avg(self):
        self.quality_rating_avg = self.calculate_quality_rating_avg()
        self.save(update_fields=["quality_rating_avg"])

    def calculate_average_response_time(self):
        average_response_time = self.purchase_orders.filter(
            status=PurchaseOrder.COMPLETED
        ).annotate(
            response_time_diff=F("acknowledgment_date") - F("issue_date"),
        ).aggregate(
            average_response_time=Avg("response_time_diff")
        )["average_response_time"]

        if average_response_time is None:
            return 0

        return average_response_time.total_seconds()

    def update_average_response_time(self):
        self.average_response_time = self.calculate_average_response_time()
        self.save(update_fields=["average_response_time"])

    def calculate_fulfillment_rate(self):
        total_orders = self.purchase_orders.count()
        completed_count = self.purchase_orders.filter(
            status=PurchaseOrder.COMPLETED
        ).count()
        if total_orders == 0:
            return 0
        return completed_count / total_orders

    def update_fulfillment_rate(self):
        self.fulfillment_rate = self.calculate_fulfillment_rate()
        self.save(update_fields=["fulfillment_rate"])

    def create_historical_performance(self):
        return HistoricalPerformance.objects.create(
            vendor=self,
            date=timezone.now(),
            on_time_delivery_rate=self.on_time_delivery_rate,
            quality_rating_avg=self.quality_rating_avg,
            average_response_time=self.average_response_time,
            fulfillment_rate=self.fulfillment_rate
        )

    def recalculate_performance_metrics(self):
        self.on_time_delivery_rate = self.calculate_on_time_delivery_rate()
        self.quality_rating_avg = self.calculate_quality_rating_avg()
        self.average_response_time = self.calculate_average_response_time()
        self.fulfillment_rate = self.calculate_fulfillment_rate()
        self.save(update_fields=[
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate"
        ])


class PurchaseOrder(models.Model):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    status_choices = (
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled")
    )

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(
        Vendor, related_name="purchase_orders", on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(choices=status_choices, max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.po_number

    def acknowledge(self):
        self.acknowledgment_date = timezone.now()
        self.save(update_fields=["acknowledgment_date"])


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        Vendor,
        related_name="historical_performances",
        on_delete=models.CASCADE
    )
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self) -> str:
        return f"{self.vendor} - {self.date}"
