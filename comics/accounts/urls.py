from django.urls import path

from comics.accounts import views

urlpatterns = [
    path(
        "",
        views.account_details,
        name="account",
    ),
    path(
        "secret-key/",
        views.secret_key,
        name="secret_key",
    ),
    path(
        "toggle-comic/",
        views.mycomics_toggle_comic,
        name="toggle_comic",
    ),
    path(
        "edit-comics/",
        views.mycomics_edit_comics,
        name="edit_comics",
    ),
    path(
        "invite/",
        views.invite,
        name="invite",
    ),
]
