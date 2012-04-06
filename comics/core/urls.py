from django.conf.urls.defaults import patterns, url

from comics.core import views

urlpatterns = patterns('',
    # Status page
    url(r'^status/$', views.status, name='status'),

    # About page
    url(r'^about/$', views.about, name='about'),

    # We do not like robots
    url(r'^robots.txt$', views.robots, name='robots'),
)
