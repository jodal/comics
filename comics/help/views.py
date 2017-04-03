from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from comics.help.forms import FeedbackForm


def about(request):
    return render(request, 'help/about.html', {
        'active': {
            'help': True,
            'about': True,
        },
    })


def feedback(request):
    """Mail feedback to ADMINS"""

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = 'Feedback from %s' % settings.COMICS_SITE_TITLE

            metadata = 'Client IP address: %s\n' % request.META['REMOTE_ADDR']
            metadata += 'User agent: %s\n' % request.META['HTTP_USER_AGENT']
            if request.user.is_authenticated:
                metadata += 'User: %s <%s>\n' % (
                    request.user.username, request.user.email)
            else:
                metadata += 'User: anonymous\n'

            message = '%s\n\n-- \n%s' % (
                form.cleaned_data['message'], metadata)

            headers = {}
            if request.user.is_authenticated:
                headers['Reply-To'] = request.user.email

            mail = EmailMessage(
                subject=subject, body=message,
                to=[email for name, email in settings.ADMINS],
                headers=headers)
            mail.send()

            messages.info(
                request,
                'Thank you for taking the time to help improve the site! :-)')
            return HttpResponseRedirect(reverse('help_feedback'))
    else:
        form = FeedbackForm()

    return render(request, 'help/feedback.html', {
        'active': {
            'help': True,
            'feedback': True,
        },
        'feedback_form': form,
    })


def keyboard(request):
    return render(request, 'help/keyboard.html', {
        'active': {
            'help': True,
            'keyboard': True,
        },
    })
