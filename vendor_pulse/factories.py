from django.contrib.auth.models import User
from django.utils import timezone

from factory import LazyAttribute
from factory.django import DjangoModelFactory
from factory.faker import Faker

from .models import (
    Vendor,
    PurchaseOrder,
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = Faker("email")
    password = Faker("password")


class AdminFactory(UserFactory):
    is_staff = True
    is_superuser = True


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
