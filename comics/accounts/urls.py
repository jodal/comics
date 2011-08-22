from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template

from registration.views import activate
from registration.views import register

urlpatterns = patterns('',
    url(r'^register/$',
        register,
        {'backend': 'registration.backends.default.DefaultBackend'},
        name='registration_register'),
    url(r'^register/complete/$',
        direct_to_template,
        {'template': 'registration/registration_complete.html'},
        name='registration_complete'),
    url(r'^register/closed/$',
        direct_to_template,
        {'template': 'registration/registration_closed.html'},
        name='registration_disallowed'),

    url(r'^activate/complete/$',
        direct_to_template,
        {'template': 'registration/activation_complete.html'},
        name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        activate,
        {'backend': 'registration.backends.default.DefaultBackend'},
        name='registration_activate'),

    url(r'^login/$',
        auth_views.login,
        {'template_name': 'auth/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'auth/logout.html'},
        name='auth_logout'),

    url(r'^password/change/$',
        auth_views.password_change,
        {'template_name': 'auth/password_change.html'},
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'auth/password_change_done.html'},
        name='auth_password_change_done'),

    url(r'^password/reset/$',
        auth_views.password_reset,
        {
            'template_name': 'auth/password_reset.html',
            'email_template_name': 'auth/password_reset_email.txt',
            'subject_template_name': 'auth/password_reset_email_subject.txt',
        },
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'auth/password_reset_confirm.html'},
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'auth/password_reset_complete.html'},
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'auth/password_done.html'},
        name='auth_password_reset_done'),
)
