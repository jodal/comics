from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from comics.accounts.models import Subscription
from comics.core.models import Comic
from comics.sets.models import Set


@login_required
def account_details(request):
    return render(request, 'accounts/details.html', {
        'active': {
            'account': True,
            'account_details': True,
        }
    })


@login_required
def secret_key(request):
    """Show and generate a new secret key for the current user"""

    if request.method == 'POST':
        comics_profile = request.user.comics_profile
        comics_profile.generate_new_secret_key()
        comics_profile.save()
        messages.info(request, 'A new secret key was generated.')
        return HttpResponseRedirect(reverse('secret_key'))

    return render(request, 'accounts/secret_key.html', {
        'active': {
            'account': True,
            'secret_key': True,
        }
    })


@login_required
def mycomics_toggle_comic(request):
    """Change a single comic in My comics"""

    if request.method != 'POST':
        response = HttpResponse(status=405)
        response['Allowed'] = 'POST'
        return response

    comic = get_object_or_404(Comic, slug=request.POST['comic'])

    if 'add_comic' in request.POST:
        subscription = Subscription(
            userprofile=request.user.comics_profile, comic=comic)
        subscription.save()
        if not request.is_ajax():
            messages.info(request, 'Added "%s" to my comics' % comic.name)
    elif 'remove_comic' in request.POST:
        subscriptions = Subscription.objects.filter(
            userprofile=request.user.comics_profile, comic=comic)
        subscriptions.delete()
        if not request.is_ajax():
            messages.info(request, 'Removed "%s" from my comics' % comic.name)

    if request.is_ajax():
        return HttpResponse(status=204)
    else:
        return HttpResponseRedirect(reverse('mycomics_latest'))


@login_required
def mycomics_edit_comics(request):
    """Change multiple comics in My comics"""

    if request.method != 'POST':
        response = HttpResponse(status=405)
        response['Allowed'] = 'POST'
        return response

    my_comics = request.user.comics_profile.comics.all()

    for comic in my_comics:
        if comic.slug not in request.POST:
            subscriptions = Subscription.objects.filter(
                userprofile=request.user.comics_profile, comic=comic)
            subscriptions.delete()
            if not request.is_ajax():
                messages.info(
                    request, 'Removed "%s" from my comics' % comic.name)

    for comic in Comic.objects.all():
        if comic.slug in request.POST and comic not in my_comics:
            subscription = Subscription(
                userprofile=request.user.comics_profile, comic=comic)
            subscription.save()
            if not request.is_ajax():
                messages.info(request, 'Added "%s" to my comics' % comic.name)

    if request.is_ajax():
        return HttpResponse(status=204)
    elif 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('mycomics_latest'))


@login_required
def mycomics_import_named_set(request):
    """Import comics from a named set into My comics"""

    if request.method == 'POST':
        try:
            named_set = Set.objects.get(name=request.POST['namedset'])
        except Set.DoesNotExist:
            messages.error(
                request,
                'No comic set named "%s" found.' % request.POST['namedset'])
            return HttpResponseRedirect(reverse('import_named_set'))

        count_before = len(request.user.comics_profile.comics.all())
        for comic in named_set.comics.all():
            Subscription.objects.get_or_create(
                userprofile=request.user.comics_profile,
                comic=comic)
        count_after = len(request.user.comics_profile.comics.all())
        count_added = count_after - count_before
        messages.info(
            request,
            '%d comic(s) was added to your comics selection.' % count_added)
        if count_added > 0:
            return HttpResponseRedirect(reverse('mycomics_latest'))
        else:
            return HttpResponseRedirect(reverse('import_named_set'))

    return render(request, 'sets/import_named_set.html', {
        'active': {
            'account': True,
            'import_named_set': True,
        }
    })
