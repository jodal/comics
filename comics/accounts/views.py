from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from comics.accounts.models import Subscription
from comics.core.models import Comic


@login_required
def account_details(request):
    return render(
        request,
        "accounts/details.html",
        {"active": {"account": True, "account_details": True}},
    )


@login_required
def secret_key(request):
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
def mycomics_toggle_comic(request):
    """Change a single comic in My comics"""

    if request.method != "POST":
        response = HttpResponse(status=405)
        response["Allowed"] = "POST"
        return response

    comic = get_object_or_404(Comic, slug=request.POST["comic"])

    if "add_comic" in request.POST:
        subscription = Subscription(
            userprofile=request.user.comics_profile, comic=comic
        )
        subscription.save()
        if not request.is_ajax():
            messages.info(request, 'Added "%s" to my comics' % comic.name)
    elif "remove_comic" in request.POST:
        subscriptions = Subscription.objects.filter(
            userprofile=request.user.comics_profile, comic=comic
        )
        subscriptions.delete()
        if not request.is_ajax():
            messages.info(request, 'Removed "%s" from my comics' % comic.name)

    if request.is_ajax():
        return HttpResponse(status=204)
    else:
        return HttpResponseRedirect(reverse("mycomics_latest"))


@login_required
def mycomics_edit_comics(request):
    """Change multiple comics in My comics"""

    if request.method != "POST":
        response = HttpResponse(status=405)
        response["Allowed"] = "POST"
        return response

    my_comics = request.user.comics_profile.comics.all()

    for comic in my_comics:
        if comic.slug not in request.POST:
            subscriptions = Subscription.objects.filter(
                userprofile=request.user.comics_profile, comic=comic
            )
            subscriptions.delete()
            if not request.is_ajax():
                messages.info(
                    request, 'Removed "%s" from my comics' % comic.name
                )

    for comic in Comic.objects.all():
        if comic.slug in request.POST and comic not in my_comics:
            subscription = Subscription(
                userprofile=request.user.comics_profile, comic=comic
            )
            subscription.save()
            if not request.is_ajax():
                messages.info(request, 'Added "%s" to my comics' % comic.name)

    if request.is_ajax():
        return HttpResponse(status=204)
    elif "HTTP_REFERER" in request.META:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        return HttpResponseRedirect(reverse("mycomics_latest"))
