from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.utils import timezone

from comics.core.models import Comic
from comics.core.utils.navigation import get_navigation
from comics.core.views import generic_show
from comics.sets.models import Set


@login_required
@never_cache
def user_set_toggle_comic(request):
    """Add to or remove from comic to the current user's set"""

    if request.method != 'POST':
        raise Http404

    comic = get_object_or_404(Comic, slug=request.POST['comic'])

    if 'add_comic' in request.POST:
        request.user_set.comics.add(comic)
        messages.info(request, 'Added "%s" to my comics' % comic.name)
    elif 'remove_comic' in request.POST:
        request.user_set.comics.remove(comic)
        messages.info(request, 'Removed "%s" from my comics' % comic.name)

    return HttpResponseRedirect(reverse('userset-latest'))


@login_required
@never_cache
def user_set_import_named_set(request):
    """Import comics from a named set into the current user's set"""

    if request.method != 'POST':
        raise Http404

    try:
        named_set = Set.objects.get(name=request.POST['namedset'])
    except Set.DoesNotExist:
        messages.error(request, 'No comic set named "%s" found.' %
            request.POST['namedset'])
        return HttpResponseRedirect(reverse('account_settings'))

    count_before = len(request.user_set.comics.all())
    request.user_set.comics.add(*named_set.comics.all())
    count_added = len(request.user_set.comics.all()) - count_before
    messages.info(request, '%d comic(s) was added to your comics selection.' %
        count_added)
    if count_added > 0:
        return HttpResponseRedirect(reverse('userset-latest'))
    else:
        return HttpResponseRedirect(reverse('account_settings'))


@login_required
@never_cache
def user_set_show(request, year=None, month=None, day=None, days=1):
    """Show comics in this user set from one or more dates"""

    year = year and int(year)
    month = month and int(month)
    day = day and int(day)
    days = days and int(days)
    if not (1 <= days <= settings.COMICS_MAX_DAYS_IN_PAGE):
        raise Http404

    queryset = request.user_set.comics.all()
    page = get_navigation(request, 'userset', instance=request.user_set,
        year=year, month=month, day=day, days=days)
    return generic_show(request, queryset, page)


@login_required
@never_cache
def user_set_latest(request):
    """Show latest releases from user set"""

    queryset = request.user_set.comics.all()
    page = get_navigation(request, 'userset', instance=request.user_set,
        days=1, latest=True)
    return generic_show(request, queryset, page, latest=True)


@login_required
def user_set_year(request, year=None):
    """Redirect to first day of year if not in the future"""

    if int(year) > timezone.now().year:
        raise Http404
    else:
        return HttpResponseRedirect(reverse('userset-date', kwargs={
            'year': year,
            'month': 1,
            'day': 1,
        }))
