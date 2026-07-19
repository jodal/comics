from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from invitations.utils import get_invitation_model

from comics.accounts.models import Subscription
from comics.core.models import Comic

if TYPE_CHECKING:
    from comics.accounts.typing import AuthenticatedHttpRequest


@login_required
def account_details(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "accounts/details.html",
        {"active": {"account": True, "account_details": True}},
    )


@login_required
def secret_key(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Show and generate a new secret key for the current user"""

    if request.method == "POST":
        comics_profile = request.user.comics_profile
        comics_profile.generate_new_secret_key()
        comics_profile.save()
        messages.info(request, "A new secret key was generated.")
        return HttpResponseRedirect(reverse("secret_key"))

    return render(
        request,
        "accounts/secret_key.html",
        {"active": {"account": True, "secret_key": True}},
    )


@login_required
def mycomics_toggle_comic(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Change a single comic in My comics"""

    if request.method != "POST":
        response = HttpResponse(status=405)
        response["Allowed"] = "POST"
        return response

    comic_slug = request.POST["comic"]
    assert isinstance(comic_slug, str)
    comic = Comic.objects.for_slug(comic_slug).get_or_404()

    if "add_comic" in request.POST:
        subscription = Subscription(
            userprofile=request.user.comics_profile, comic=comic
        )
        subscription.save()
        if not _is_js_request(request):
            messages.info(request, f'Added "{comic.name}" to my comics')
    elif "remove_comic" in request.POST:
        subscriptions = Subscription.objects.for_user(request.user).for_comic(comic)
        subscriptions.delete()
        if not _is_js_request(request):
            messages.info(request, f'Removed "{comic.name}" from my comics')

    if _is_js_request(request):
        return HttpResponse(status=204)
    else:
        return HttpResponseRedirect(reverse("mycomics_latest"))


@login_required
def mycomics_edit_comics(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Change multiple comics in My comics"""

    if request.method != "POST":
        response = HttpResponse(status=405)
        response["Allowed"] = "POST"
        return response

    my_comics = request.user.comics_profile.comics.all()

    for comic in my_comics:
        if comic.slug not in request.POST:
            subscriptions = Subscription.objects.for_user(request.user).for_comic(comic)
            subscriptions.delete()
            if not _is_js_request(request):
                messages.info(request, f'Removed "{comic.name}" from my comics')

    for comic in Comic.objects.all():
        if comic.slug in request.POST and comic not in my_comics:
            subscription = Subscription(
                userprofile=request.user.comics_profile, comic=comic
            )
            subscription.save()
            if not _is_js_request(request):
                messages.info(request, f'Added "{comic.name}" to my comics')

    if _is_js_request(request):
        return HttpResponse(status=204)
    elif "referer" in request.headers:
        return HttpResponseRedirect(request.headers["referer"])
    else:
        return HttpResponseRedirect(reverse("mycomics_latest"))


@login_required
def invite(request: AuthenticatedHttpRequest) -> HttpResponse:
    if request.method == "POST":
        invitation_model = get_invitation_model()
        email = request.POST["email"]
        assert isinstance(email, str)
        invitation = invitation_model.create(email, inviter=request.user)
        invitation.send_invitation(request)
        messages.success(
            request, f'An invitation has been sent to "{invitation.email}".'
        )

    invitations = request.user.invitation_set.all().order_by("-created")

    return render(
        request,
        "accounts/invite.html",
        {
            "active": {"invite": True},
            "invitations": invitations,
        },
    )


def _is_js_request(request: HttpRequest) -> bool:
    return request.headers.get("JS-Request") == "true"
