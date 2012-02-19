from django.conf import settings
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from comics.feedback.forms import FeedbackForm

def feedback(request):
    """Mail feedback to ADMINS"""

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = 'Feedback from %s' % settings.COMICS_SITE_TITLE
            message = form.cleaned_data['message']

            metadata = 'Client IP address: %s\n' % request.META['REMOTE_ADDR']
            metadata += 'User agent: %s\n' % request.META['HTTP_USER_AGENT']
            if request.user.is_authenticated():
                metadata += 'User: %s <%s>\n' % (
                    request.user.username, request.user.email)
            else:
                metadata += 'User: anonymous\n'
            message = '%s\n\n%s' % (message, metadata)

            mail_admins(subject, message)
            return HttpResponseRedirect(reverse('feedback-thanks'))
    else:
        form = FeedbackForm()

    return render(request, 'feedback/form.html', {
        'active': {'feedback': True},
        'feedback_form': form,
    })

def feedback_thanks(request):
    """Display form submit confirmation page"""

    return render(request, 'feedback/thanks.html')
