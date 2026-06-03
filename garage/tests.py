"""
Tests = automated checks so you do not break things while learning.

Run: python manage.py test

Exercise: add tests when you finish Exercise 10 (formset save).
"""

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .models import LineItem, MaintenanceEvent, Motorcycle, ServiceType


class LineItemAmountTests(TestCase):
    def test_amount_is_quantity_times_unit_cost(self):
        user = User.objects.create_user("tester", password="test-pass-123")
        bike = Motorcycle.objects.create(
            user=user,
            brand="Yamaha",
            model="MT-03",
            year=2021,
        )
        event = MaintenanceEvent.objects.create(
            motorcycle=bike,
            service_date="2025-01-15",
            odometer_km=5000,
            title="Chain lube",
            service_type=ServiceType.DIY,
        )
        item = LineItem.objects.create(
            event=event,
            description="Chain lube spray",
            quantity=Decimal("1"),
            unit_cost=Decimal("299.00"),
        )
        self.assertEqual(item.amount, Decimal("299.00"))
