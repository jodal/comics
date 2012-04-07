from django.conf.urls.defaults import patterns, url

from comics.status import views

urlpatterns = patterns('',
    url(r'^$', views.status, name='status'),
)
