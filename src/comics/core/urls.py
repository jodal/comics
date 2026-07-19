from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import path

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def fail(request: HttpRequest) -> HttpResponse:
    # Useful for e.g. testing Sentry integration
    raise ZeroDivisionError("division by zero")


urlpatterns = [
    path("fail/", fail),
]
