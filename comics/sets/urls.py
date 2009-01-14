from django.conf.urls.defaults import *

from comics.sets import views

urlpatterns = patterns('',
    # Comic sets
    url(r'^$',
        views.set_new, name='set-new'),
    url(r'^(?P<set>[0-9a-z-_]+)/edit/$',
        views.set_edit, name='set-edit'),

    url(r'^(?P<set>[0-9a-z-_]+)/$',
        views.set_latest, name='set-latest'),
    url(r'^(?P<set>[0-9a-z-_]+)/\+(?P<days>\d+)/$',
        views.set_show, name='set-last-days'),
    url(r'^(?P<set>[0-9a-z-_]+)/(?P<year>\d{4})/$',
        views.set_year, name='set-year'),
    url(r'^(?P<set>[0-9a-z-_]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.set_show, name='set-month'),
    url(r'^(?P<set>[0-9a-z-_]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.set_show, name='set-date'),
    url(r'^(?P<set>[0-9a-z-_]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/\+(?P<days>\d+)/$',
        views.set_show, name='set-date-days'),
)
