from django.conf.urls.defaults import *
from haystack.views import SearchView
from haystack.forms import SearchForm

search_view = SearchView(form_class=SearchForm, load_all=False)

urlpatterns = patterns('',
    url(r'^$', search_view, name='search'),
)
