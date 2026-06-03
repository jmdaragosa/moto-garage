"""
Django Forms = HTML forms + validation, backed by your models.

This file is intentionally mostly empty. You will build forms in docs/YOUR_TURN.md
(Exercises 5–7). Start by reading:
  https://docs.djangoproject.com/en/stable/topics/forms/
  https://docs.djangoproject.com/en/stable/topics/forms/modelforms/
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Motorcycle, MaintenanceEvent, LineItem

class MotorcycleForm(forms.ModelForm):
     class Meta:
         model = Motorcycle
         fields = ["brand", "model", "year", "nickname", "vin", "current_odometer_km", "notes"]
         widgets = {"notes": forms.Textarea(attrs={"rows": 4}),
                    }

class MaintenanceEventForm(forms.ModelForm):
     class Meta:
          model = MaintenanceEvent
          exclude = ["motorcycle", "created_at", "updated_at"]
          widgets = {
               "service_date": forms.DateInput(attrs={"type": "date"}),
               "notes": forms.Textarea(attrs={"rows": 4}),
          }

LineItemFormSet = inlineformset_factory(
     MaintenanceEvent,
     LineItem,

     fields=["kind", "description","quantity", "unit_cost", "vendor"],
     extra=1,
     can_delete=False,
)