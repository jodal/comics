from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template

from registration.views import activate, register

from comics.accounts.forms import (AuthenticationForm, PasswordChangeForm,
    PasswordResetForm)
from comics.accounts.views import new_secret_key
from comics.sets.views import user_set_toggle_comic

urlpatterns = patterns('',
    url(r'^register/$',
        register,
        {
            'backend': 'comics.accounts.backends.RegistrationBackend',
            'extra_context': {'active': {'register': True}},
        },
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
        {'backend': 'comics.accounts.backends.RegistrationBackend'},
        name='registration_activate'),

    url(r'^login/$',
        auth_views.login,
        {
            'authentication_form': AuthenticationForm,
            'extra_context': {'active': {'login': True}},
            'template_name': 'auth/login.html',
        },
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'next_page': '/account/login/'},
        name='auth_logout'),

    url(r'^$',
        direct_to_template,
        {
            'template': 'accounts/settings.html',
            'extra_context': {'active': {'account': True}},
        },
        name='account_settings'),

    url(r'^password/change/$',
        auth_views.password_change,
        {
            'template_name': 'auth/password_change.html',
            'password_change_form': PasswordChangeForm,
        },
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
            # XXX The next line is not supported until Django 1.4
            #'subject_template_name': 'auth/password_reset_email_subject.txt',
            'password_reset_form': PasswordResetForm,
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
        {'template_name': 'auth/password_reset_done.html'},
        name='auth_password_reset_done'),

    url(r'^key/$', new_secret_key, name='new_secret_key'),

    url(r'^toggle-comic/$', user_set_toggle_comic, name='toggle_comic'),
)
