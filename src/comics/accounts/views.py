from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST
from invitations.utils import get_invitation_model

from comics.accounts.services import SubscriptionService
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
@require_POST
def mycomics_toggle_comic(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Change a single comic in My comics"""

    comic_slug = request.POST.get("comic")
    if not comic_slug:
        return HttpResponseBadRequest("Missing 'comic' parameter")
    comic = Comic.objects.for_slug(comic_slug).get_or_404()

    if "add_comic" in request.POST:
        SubscriptionService.subscribe(user=request.user, comic=comic)
        if not _is_js_request(request):
            messages.info(request, f'Added "{comic.name}" to my comics')
    elif "remove_comic" in request.POST:
        SubscriptionService.unsubscribe(user=request.user, comic=comic)
        if not _is_js_request(request):
            messages.info(request, f'Removed "{comic.name}" from my comics')

    if _is_js_request(request):
        return HttpResponse(status=204)
    else:
        return HttpResponseRedirect(reverse("mycomics_latest"))


@login_required
@require_POST
def mycomics_edit_comics(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Change multiple comics in My comics"""

    my_comics = request.user.comics_profile.comics.all()

    for comic in my_comics:
        if comic.slug not in request.POST:
            SubscriptionService.unsubscribe(user=request.user, comic=comic)
            if not _is_js_request(request):
                messages.info(request, f'Removed "{comic.name}" from my comics')

    for comic in Comic.objects.all():
        if comic.slug in request.POST and comic not in my_comics:
            SubscriptionService.subscribe(user=request.user, comic=comic)
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
        email = request.POST.get("email")
        if not email:
            return HttpResponseBadRequest("Missing 'email' parameter")
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
