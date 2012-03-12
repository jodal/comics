from django.conf.urls.defaults import patterns, url

from comics.feedback import views

urlpatterns = patterns('',
    # Feedback form
    url(r'^$', views.feedback, name='feedback'),
    url(r'^thanks/$', views.feedback_thanks, name='feedback-thanks'),
)
