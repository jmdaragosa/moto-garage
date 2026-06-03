from django.urls import path
from garage.views.motorcycle import MotorcycleCreateView, MotorcycleListView, MotorcycleDetailView
from garage.views.service import MaintenanceEventCreateView

from . import views

app_name = "garage"

urlpatterns = [
    path("", views.home, name="home"),
    path("motorcycles/", MotorcycleListView.as_view(), name="motorcycle_list",),
    path("motorcycles/new/", MotorcycleCreateView.as_view(), name="motorcycle_create",),
    path("motocycle/<int:pk>/", MotorcycleDetailView.as_view(), name="motorcycle_detail",),
    path("motocycle/<int:pk>/services/new/", MaintenanceEventCreateView.as_view(), name="service_create",),
]