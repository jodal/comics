from django.conf.urls import patterns, url

from comics.help import views

urlpatterns = patterns(
    '',

    url(r'^$', views.about, name='help_about'),
    url(r'^feedback/$', views.feedback, name='help_feedback'),
    url(r'^keyboard/$', views.keyboard, name='help_keyboard'),
)
