from django.urls import path

from comics.help import views

urlpatterns = [
    path("", views.about, name="help_about"),
    path("feedback/", views.feedback, name="help_feedback"),
    path("keyboard/", views.keyboard, name="help_keyboard"),
]
