from django.urls import path
from garage.views.motorcycle import MotorcycleCreateView, MotorcycleListView, MotorcycleDetailView
from garage.views.service import MaintenanceEventCreateView
from garage.views.auth import signup_view
from django.contrib.auth.views import LogoutView, LoginView

from . import views

app_name = "garage"

urlpatterns = [
    path("", views.home, name="home"),
    path("motorcycles/", MotorcycleListView.as_view(), name="motorcycle_list",),
    path("motorcycles/new/", MotorcycleCreateView.as_view(), name="motorcycle_create",),
    path("motorcycle/<int:pk>/", MotorcycleDetailView.as_view(), name="motorcycle_detail",),
    path("motorcycle/<int:pk>/services/new/", MaintenanceEventCreateView.as_view(), name="service_create",),
    path("signup/", signup_view, name="signup",),
    path("accounts/logout/",LogoutView.as_view(), name="logout",),
    path("accounts/login/", LoginView.as_view(), name="login",),
]