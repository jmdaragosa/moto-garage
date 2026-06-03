from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from garage.forms import MaintenanceEventForm, LineItemFormSet
from garage.models import Motorcycle


class MaintenanceEventCreateView(LoginRequiredMixin, View):

    template_name = "garage/service_form.html"

    def get_motorcycle(self):
        return get_object_or_404(
            Motorcycle,
            pk=self.kwargs["pk"],
            user=self.request.user,
        )

    def get(self, request, *args, **kwargs):
        form = MaintenanceEventForm()
        formset = LineItemFormSet()

        return render(
            request,
            self.template_name,
            {
                "bike": self.get_motorcycle(),
                "form": form,
                "formset": formset,
            },
        )

    def post(self, request, *args, **kwargs):
        bike = self.get_motorcycle()

        form = MaintenanceEventForm(request.POST)
        formset = LineItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():

            event = form.save(commit=False)
            event.motorcycle = bike
            event.save()

            formset.instance = event
            formset.save()

            return redirect(
                "garage:motorcycle_detail",
                pk=bike.pk,
            )

        return render(
            request,
            self.template_name,
            {
                "bike": bike,
                "form": form,
                "formset": formset,
            },
        )