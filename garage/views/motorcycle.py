from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from django.db.models import Sum
from decimal import Decimal

from garage.forms import MotorcycleForm
from garage.models import Motorcycle


class MotorcycleCreateView(LoginRequiredMixin, CreateView):
    model = Motorcycle
    form_class = MotorcycleForm
    template_name = "garage/motorcycle_form.html"
    success_url = reverse_lazy("garage:home")  # change if needed

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MotorcycleListView(LoginRequiredMixin, ListView):
    model = Motorcycle
    template_name = "garage/motorcycle_list.html"
    context_object_name = "bikes"

    def get_queryset(self):
        return Motorcycle.objects.filter(user=self.request.user)
    
class MotorcycleDetailView(LoginRequiredMixin, DetailView):
    model = Motorcycle
    template_name = "garage/motorcycle_detail.html"
    context_object_name = "bike"

    def get_queryset(self):
        return Motorcycle.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = self.object.maintenance_events.all()
        total = events.aggregate(s=Sum("line_items__amount"))["s"] or Decimal("0.00")
        context["lifetime_spend"] = total
        return context