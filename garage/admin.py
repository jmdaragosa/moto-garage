"""
Django Admin = auto-generated CRUD UI for staff users.

YOUR JOB later: build *your* UI in views/templates. Until then, use admin to
log real maintenance and validate the data model.

Docs: https://docs.djangoproject.com/en/stable/ref/contrib/admin/
"""

from django.contrib import admin

from .models import LineItem, MaintenanceEvent, Motorcycle


class LineItemInline(admin.TabularInline):
    """Edit line items on the same page as the maintenance event."""

    model = LineItem
    extra = 1  # one blank row for quick entry


@admin.register(Motorcycle)
class MotorcycleAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "nickname", "current_odometer_km", "user")
    list_filter = ("brand", "year")
    search_fields = ("brand", "model", "nickname", "vin")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(MaintenanceEvent)
class MaintenanceEventAdmin(admin.ModelAdmin):
    list_display = (
        "service_date",
        "title",
        "motorcycle",
        "service_type",
        "odometer_km",
        "total_php",
    )
    list_filter = ("service_type", "service_date")
    search_fields = ("title", "shop_name", "notes")
    inlines = [LineItemInline]
    date_hierarchy = "service_date"

    @admin.display(description="Total (PHP)")
    def total_php(self, obj: MaintenanceEvent):
        return obj.total_php


@admin.register(LineItem)
class LineItemAdmin(admin.ModelAdmin):
    list_display = ("description", "kind", "quantity", "unit_cost", "amount", "event")
    list_filter = ("kind",)
