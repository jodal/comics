from django.conf.urls.defaults import patterns, url

from comics.feedback import views

urlpatterns = patterns('',
    # Feedback form
    url(r'^$', views.feedback, name='feedback'),
)
