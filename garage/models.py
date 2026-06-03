"""
Domain models for moto-garage.

Read top-to-bottom once, then open docs/LEARN.md § "Models".
Key ideas:
  - Models = Python classes that map to database tables.
  - ForeignKey = "many of these belong to one of those" (e.g. many events per motorcycle).
  - TextChoices = constrained string values stored in the DB (diy vs shop).
"""

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum


class ServiceType(models.TextChoices):
    """Where the work happened — you pick this per maintenance event."""

    DIY = "diy", "DIY"
    SHOP = "shop", "Shop"


class LineItemKind(models.TextChoices):
    """What kind of money left your wallet on this line."""

    PART = "part", "Part"
    LABOR = "labor", "Labor"
    FEE = "fee", "Fee"
    OTHER = "other", "Other"


class Motorcycle(models.Model):
    """
    One bike you own. A user can have many (Multi-Motorcycle requirement).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="motorcycles",
    )
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    nickname = models.CharField(max_length=100, blank=True)
    vin = models.CharField("VIN", max_length=50, blank=True)
    current_odometer_km = models.PositiveIntegerField(
        default=0,
        help_text="Latest known odometer reading in kilometers.",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["brand", "model", "-year"]

    def __str__(self) -> str:
        label = f"{self.year} {self.brand} {self.model}"
        if self.nickname:
            return f"{label} ({self.nickname})"
        return label


class MaintenanceEvent(models.Model):
    """
    One service visit or DIY session on a motorcycle.
    Line items (parts, labor) hang off this via ForeignKey.
    """

    motorcycle = models.ForeignKey(
        Motorcycle,
        on_delete=models.CASCADE,
        related_name="maintenance_events",
    )
    service_date = models.DateField()
    odometer_km = models.PositiveIntegerField(
        help_text="Odometer reading when this service was done.",
    )
    title = models.CharField(max_length=200)
    service_type = models.CharField(
        max_length=10,
        choices=ServiceType.choices,
        default=ServiceType.DIY,
    )
    shop_name = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-service_date", "-created_at"]

    def __str__(self) -> str:
        return f"{self.service_date} — {self.title}"

    def clean(self) -> None:
        """
        Model-level validation (runs in forms/admin before save).
        Try: set service_type=shop and leave shop_name blank in admin — you should see an error.
        """
        super().clean()
        if self.service_type == ServiceType.SHOP and not self.shop_name.strip():
            raise ValidationError(
                {"shop_name": "Shop name is required when service type is Shop."}
            )

    @property
    def total_php(self) -> Decimal:
        """Sum of all line items. Used in admin list_display and your templates later."""
        total = self.line_items.aggregate(s=Sum("amount"))["s"]
        return total or Decimal("0.00")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Keep motorcycle odometer in sync if this reading is higher.
        bike = self.motorcycle
        if self.odometer_km > bike.current_odometer_km:
            bike.current_odometer_km = self.odometer_km
            bike.save(update_fields=["current_odometer_km", "updated_at"])


class LineItem(models.Model):
    """
  One row on a "receipt": a part, labor charge, fee, etc.
  amount is derived from quantity × unit_cost — see save().
  """

    event = models.ForeignKey(
        MaintenanceEvent,
        on_delete=models.CASCADE,
        related_name="line_items",
    )
    kind = models.CharField(
        max_length=10,
        choices=LineItemKind.choices,
        default=LineItemKind.PART,
    )
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("1.00"))
    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Price per unit in PHP.",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False,
        help_text="Computed: quantity × unit_cost.",
    )
    vendor = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.get_kind_display()}: {self.description}"

    def save(self, *args, **kwargs):
        # Always recompute so admin/imports cannot store wrong totals.
        self.amount = (self.quantity * self.unit_cost).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)
