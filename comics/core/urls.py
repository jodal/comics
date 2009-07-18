from django.conf.urls.defaults import *

from comics.core import views

urlpatterns = patterns('',
    # View top comics
    url(r'^$',
        views.top_latest, name='top-latest'),
    url(r'^\+(?P<days>\d+)/$',
        views.top_show, name='top-last-days'),
    url(r'^(?P<year>\d{4})/$',
        views.top_year, name='top-year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.top_show, name='top-month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.top_show, name='top-date'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/\+(?P<days>\d+)/$',
        views.top_show, name='top-date-days'),

    # View one specific comic
    url(r'^c/$',
        views.comic_list, name='comic-list'),
    url(r'^c/(?P<comic>[0-9a-z-_]+)/$',
        views.comic_latest, name='comic-latest'),
    url(r'^c/(?P<comic>[0-9a-z-_]+)/\+(?P<days>\d+)/$',
        views.comic_show, name='comic-last-days'),
    url(r'^c/(?P<comic>[0-9a-z-_]+)/(?P<year>\d{4})/$',
        views.comic_year, name='comic-year'),
    url(r'^c/(?P<comic>[0-9a-z-_]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.comic_show, name='comic-month'),
    url(r'^c/(?P<comic>[0-9a-z-_]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.comic_show, name='comic-date'),
    url(r'^c/(?P<comic>[0-9a-z-_]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/\+(?P<days>\d+)/$',
        views.comic_show, name='comic-date-days'),

    # About page
    url(r'^about/$', views.about, name='about'),

    # We do not like robots
    url(r'^robots.txt$', views.robots, name='robots'),
)
