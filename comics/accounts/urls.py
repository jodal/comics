from django.conf.urls import url

from comics.accounts import views as account_views

urlpatterns = [
    url(r"^$", account_views.account_details, name="account"),
    url(r"^secret-key/$", account_views.secret_key, name="secret_key"),
    url(
        r"^toggle-comic/$",
        account_views.mycomics_toggle_comic,
        name="toggle_comic",
    ),
    url(
        r"^edit-comics/$",
        account_views.mycomics_edit_comics,
        name="edit_comics",
    ),
    url(
        r"^invite/$",
        account_views.invite,
        name="invite",
    ),
]
