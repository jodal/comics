from django.conf.urls.defaults import *

from comics.core.urls import YEAR, MONTH, DAY, DAYS
from comics.sets import views

SET = r'(?P<set>[0-9a-z-_]+)'

urlpatterns = patterns('',
    # Comic sets
    url(r'^$',
        views.set_new, name='set-new'),
    url(r'^%s/edit/$' % (SET,),
        views.set_edit, name='set-edit'),

    url(r'^%s/$' % (SET,),
        views.set_latest, name='set-latest'),
    url(r'^%s/%s/$' % (SET, DAYS),
        views.set_show, name='set-last-days'),
    url(r'^%s/%s/$' % (SET, YEAR),
        views.set_year, name='set-year'),
    url(r'^%s/%s/%s/$' % (SET, YEAR, MONTH),
        views.set_show, name='set-month'),
    url(r'^%s/%s/%s/%s/$' % (SET, YEAR, MONTH, DAY),
        views.set_show, name='set-date'),
    url(r'^%s/%s/%s/%s/%s/$' % (SET, YEAR, MONTH, DAY, DAYS),
        views.set_show, name='set-date-days'),
)
