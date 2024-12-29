from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from comics.help.forms import FeedbackForm


def about(request):
    return render(request, "help/about.html", {"active": {"help": True, "about": True}})


@login_required
def feedback(request):
    """Mail feedback to ADMINS"""

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = "Feedback from %s" % settings.COMICS_SITE_TITLE

            metadata = "Client IP address: %s\n" % request.META["REMOTE_ADDR"]
            metadata += "User agent: %s\n" % request.headers["user-agent"]
            metadata += f"User: {request.user.username} <{request.user.email}>\n"

            message = "{}\n\n-- \n{}".format(form.cleaned_data["message"], metadata)

            mail = EmailMessage(
                subject=subject,
                body=message,
                to=[email for name, email in settings.ADMINS],
                headers={"Reply-To": request.user.email},
            )
            mail.send()

            messages.info(
                request,
                "Thank you for taking the time to help improve the site! :-)",
            )
            return HttpResponseRedirect(reverse("help_feedback"))
    else:
        form = FeedbackForm()

    return render(
        request,
        "help/feedback.html",
        {"active": {"help": True, "feedback": True}, "feedback_form": form},
    )


def keyboard(request):
    return render(
        request,
        "help/keyboard.html",
        {"active": {"help": True, "keyboard": True}},
    )
