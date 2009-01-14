from django.conf import settings
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from comics.feedback.forms import FeedbackForm

def feedback(request):
    """Mail feedback to ADMINS"""

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = 'Feedback from %s' % settings.COMICS_SITE_TITLE
            message = form.cleaned_data['message']
            mail_admins(subject, message)
            return HttpResponseRedirect(reverse('feedback-thanks'))
    else:
        form = FeedbackForm()

    return render_to_response('feedback/form.html', {
        'feedback_form': form,
    }, context_instance=RequestContext(request))

def feedback_thanks(request):
    """Display form submit confirmation page"""

    return render_to_response('feedback/thanks.html',
        context_instance=RequestContext(request))
