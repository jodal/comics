from django.conf.urls import patterns, url

from comics.status import views

urlpatterns = patterns(
    '',
    url(r'^$', views.status, name='status'),
)
