from django.conf.urls.defaults import *

from comics.core.urls import YEAR, MONTH, DAY, DAYS
from comics.sets import views

SET = r'(?P<namedset>[0-9a-z-_]+)'

urlpatterns = patterns('',
    # Named comic sets
    url(r'^$',
        views.named_set_new, name='namedset-new'),
    url(r'^%s/edit/$' % (SET,),
        views.named_set_edit, name='namedset-edit'),
    url(r'^%s/$' % (SET,),
        views.named_set_latest, name='namedset-latest'),
    url(r'^%s/%s/$' % (SET, DAYS),
        views.named_set_show, name='namedset-last-days'),
    url(r'^%s/%s/$' % (SET, YEAR),
        views.named_set_year, name='namedset-year'),
    url(r'^%s/%s/%s/$' % (SET, YEAR, MONTH),
        views.named_set_show, name='namedset-month'),
    url(r'^%s/%s/%s/%s/$' % (SET, YEAR, MONTH, DAY),
        views.named_set_show, name='namedset-date'),
    url(r'^%s/%s/%s/%s/%s/$' % (SET, YEAR, MONTH, DAY, DAYS),
        views.named_set_show, name='namedset-date-days'),
)
