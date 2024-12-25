from django.urls import path

from comics.status import views

urlpatterns = [
    path("", views.status, name="status"),
]
