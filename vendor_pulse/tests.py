from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIRequestFactory, force_authenticate

from .factories import (
    VendorFactory,
    PurchaseOrderFactory,
    AdminFactory,
)
from .models import PurchaseOrder
from .serializers import VendorSerializer
from .views import VendorModelViewSet


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

        self.purchase_order_2.delivery_date = (
            timezone.now() +
            timezone.timedelta(days=1)
        )
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

        self.assertEqual(round(calculated_avg_1, 2), round(avg_1, 2))

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
        self.assertEqual(round(calculated_avg_2, 2), round(avg_2, 2))

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


class VendorModelViewSetTests(TestCase):
    def setUp(self):
        self.api_factory = APIRequestFactory()
        self.admin_user = AdminFactory()
        self.vendor_1 = VendorFactory()
        self.vendor_2 = VendorFactory()

    def test_vendor_list(self):
        request = self.api_factory.get("/vendors/")
        view = VendorModelViewSet.as_view({"get": "list"})
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        current_response = response.data
        expected_response = VendorSerializer(
            [self.vendor_1, self.vendor_2], many=True
        ).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(current_response, expected_response)

    def test_vendor_retrieve(self):
        request = self.api_factory.get("/vendors/")
        view = VendorModelViewSet.as_view({"get": "retrieve"})
        force_authenticate(request, user=self.admin_user)
        response = view(request, pk=self.vendor_1.pk)
        current_response = response.data
        expected_response = VendorSerializer(self.vendor_1).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_response, expected_response)

    def test_vendor_performance(self):
        request = self.api_factory.get("/vendors/")
        view = VendorModelViewSet.as_view({"get": "performance"})
        force_authenticate(request, user=self.admin_user)
        response = view(request, pk=self.vendor_1.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["on_time_delivery_rate"], 0.0)
        self.assertEqual(response.data["quality_rating_avg"], 0.0)
        self.assertEqual(response.data["average_response_time"], 0.0)
        self.assertEqual(response.data["fulfillment_rate"], 0.0)

        self.purchase_order_1_1 = PurchaseOrderFactory(vendor=self.vendor_1)
        self.purchase_order_1_1.status = PurchaseOrder.COMPLETED
        self.purchase_order_1_1.save()

        self.purchase_order_1_2 = PurchaseOrderFactory(vendor=self.vendor_1)
        self.purchase_order_1_2.status = PurchaseOrder.COMPLETED
        self.purchase_order_1_2.save()

        request = self.api_factory.get("/vendors/")
        view = VendorModelViewSet.as_view({"get": "performance"})
        force_authenticate(request, user=self.admin_user)
        response = view(request, pk=self.vendor_1.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["on_time_delivery_rate"], 1.0)
        self.assertEqual(response.data["quality_rating_avg"], 0.0)
        self.assertEqual(response.data["average_response_time"], 0.0)
        self.assertEqual(response.data["fulfillment_rate"], 1.0)

        self.purchase_order_1_1.quality_rating = 3
        self.purchase_order_1_1.save()

        self.purchase_order_1_2.quality_rating = 5
        self.purchase_order_1_2.save()

        request = self.api_factory.get("/vendors/")
        view = VendorModelViewSet.as_view({"get": "performance"})
        force_authenticate(request, user=self.admin_user)
        response = view(request, pk=self.vendor_1.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["on_time_delivery_rate"], 1.0)
        self.assertEqual(response.data["quality_rating_avg"], 4.0)
        self.assertEqual(response.data["average_response_time"], 0.0)
        self.assertEqual(response.data["fulfillment_rate"], 1.0)

        self.purchase_order_1_1.issue_date = timezone.now()
        self.purchase_order_1_1.acknowledgment_date = (
            timezone.now() +
            timezone.timedelta(seconds=5)
        )
        self.purchase_order_1_1.save()

        self.purchase_order_1_2.issue_date = timezone.now()
        self.purchase_order_1_2.acknowledgment_date = (
            timezone.now() +
            timezone.timedelta(seconds=10)
        )
        self.purchase_order_1_2.save()

        request = self.api_factory.get("/vendors/")
        view = VendorModelViewSet.as_view({"get": "performance"})
        force_authenticate(request, user=self.admin_user)
        response = view(request, pk=self.vendor_1.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["on_time_delivery_rate"], 1.0)
        self.assertEqual(response.data["quality_rating_avg"], 4.0)
        self.assertEqual(round(response.data["average_response_time"], 2), 7.5)
        self.assertEqual(response.data["fulfillment_rate"], 1.0)
