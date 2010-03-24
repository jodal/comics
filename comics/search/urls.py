from django.conf.urls.defaults import *
from haystack.views import SearchView
from haystack.forms import SearchForm

urlpatterns = patterns('',
    url(r'^$', SearchView(form_class=SearchForm), name='search'),
)
