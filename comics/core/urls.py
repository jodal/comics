from django.conf.urls.defaults import patterns, url

from comics.core import views

urlpatterns = patterns('',
    url(r'^robots.txt$', views.robots, name='robots'),
)
