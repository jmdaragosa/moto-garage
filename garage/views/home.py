from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """
    Temporary landing page until you build the real dashboard (Exercise 8).
    """
    return render(
        request,
        "garage/home.html",
        {
            "title": "Moto Garage",
        },
    )