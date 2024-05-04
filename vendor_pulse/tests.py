from django.test import TestCase
from django.utils import timezone
from django.db.models import Avg, F

from factory import LazyAttribute
from factory.django import DjangoModelFactory
from factory.faker import Faker

from .models import (
    Vendor,
    PurchaseOrder,
)


class VendorFactory(DjangoModelFactory):
    class Meta:
        model = Vendor

    name = Faker("company")
    contact_details = Faker("phone_number")
    address = Faker("address")
    vendor_code = Faker("uuid4")


class PurchaseOrderFactory(DjangoModelFactory):
    class Meta:
        model = PurchaseOrder

    po_number = Faker("uuid4")
    vendor = VendorFactory()
    order_date = LazyAttribute(
        lambda o: timezone.now() - timezone.timedelta(days=5))
    delivery_date = LazyAttribute(
        lambda o: timezone.now() - timezone.timedelta(days=3))
    items = []
    quantity = 0
    status = PurchaseOrder.PENDING


class VendorTests(TestCase):
    def setUp(self):
        self.vendor = VendorFactory()
        self.purchase_order_1 = PurchaseOrderFactory(vendor=self.vendor)
        self.purchase_order_2 = PurchaseOrderFactory(vendor=self.vendor)

    def test_calculate_on_time_delivery_rate(self):
        self.assertEqual(self.vendor.calculate_on_time_delivery_rate(), 0.0)
        self.purchase_order_1.status = PurchaseOrder.COMPLETED
        self.purchase_order_1.save()
        self.assertEqual(self.vendor.calculate_on_time_delivery_rate(), 1.0)

        self.purchase_order_2.status = PurchaseOrder.COMPLETED
        self.purchase_order_2.save()
        self.assertEqual(self.vendor.calculate_on_time_delivery_rate(), 1.0)

        self.purchase_order_2.delivery_date = timezone.now() + timezone.timedelta(days=1)
        self.purchase_order_2.save()
        self.assertEqual(self.vendor.calculate_on_time_delivery_rate(), 0.5)

    def test_calculate_quality_rating_avg(self):
        self.assertEqual(self.vendor.calculate_quality_rating_avg(), 0.0)

        self.purchase_order_1.quality_rating = 5
        self.purchase_order_1.status = PurchaseOrder.COMPLETED
        self.purchase_order_1.save()
        self.assertEqual(self.vendor.calculate_quality_rating_avg(), 5.0)

        self.purchase_order_2.quality_rating = 3
        self.purchase_order_2.status = PurchaseOrder.COMPLETED
        self.purchase_order_2.save()
        self.assertEqual(self.vendor.calculate_quality_rating_avg(), 4.0)

        self.purchase_order_2.status = PurchaseOrder.PENDING
        self.purchase_order_2.save()
        self.assertEqual(self.vendor.calculate_quality_rating_avg(), 5.0)

        self.purchase_order_2.status = PurchaseOrder.CANCELLED
        self.purchase_order_2.save()
        self.assertEqual(self.vendor.calculate_quality_rating_avg(), 5.0)

    def test_calculate_average_response_time(self):
        self.assertEqual(self.vendor.calculate_average_response_time(), 0.0)

        current_time = timezone.now()
        self.purchase_order_1.acknowledgment_date = (
            current_time +
            timezone.timedelta(seconds=5)
        )
        self.purchase_order_1.save()

        calculated_avg_1 = self.vendor.calculate_average_response_time()
        avg_1 = (
            self.purchase_order_1.acknowledgment_date -
            self.purchase_order_1.issue_date
        ).total_seconds() / 1

        self.assertEqual(round(calculated_avg_1, 3), round(avg_1, 3))

        self.purchase_order_2.acknowledgment_date = (
            current_time +
            timezone.timedelta(seconds=10)
        )
        self.purchase_order_2.save()

        calculated_avg_2 = self.vendor.calculate_average_response_time()
        avg_2 = (
            (
                self.purchase_order_2.acknowledgment_date -
                self.purchase_order_2.issue_date
            ).total_seconds() +
            (
                self.purchase_order_1.acknowledgment_date -
                self.purchase_order_2.issue_date
            ).total_seconds()
        ) / 2
        self.assertEqual(round(calculated_avg_2, 3), round(avg_2, 3))

    def test_calculate_fulfillment_rate(self):
        self.assertEqual(self.vendor.calculate_fulfillment_rate(), 0.0)

        self.purchase_order_1.status = PurchaseOrder.COMPLETED
        self.purchase_order_1.save()
        self.assertEqual(self.vendor.calculate_fulfillment_rate(), 0.5)

        self.purchase_order_2.status = PurchaseOrder.COMPLETED
        self.purchase_order_2.save()
        self.assertEqual(self.vendor.calculate_fulfillment_rate(), 1.0)

        self.purchase_order_2.status = PurchaseOrder.CANCELLED
        self.purchase_order_2.save()
        self.assertEqual(self.vendor.calculate_fulfillment_rate(), 0.5)

        self.purchase_order_2.status = PurchaseOrder.PENDING
        self.purchase_order_2.save()
        self.assertEqual(self.vendor.calculate_fulfillment_rate(), 0.5)
