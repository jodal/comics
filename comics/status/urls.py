from django.conf.urls import url

from comics.status import views

urlpatterns = [
    url(r'^$', views.status, name='status'),
]
