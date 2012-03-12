import datetime as dt

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.views.decorators.cache import never_cache

from comics.core.models import Comic
from comics.core.utils.navigation import get_navigation
from comics.core.views import generic_show
from comics.sets.models import NamedSet, UserSet
from comics.sets.forms import NewNamedSetForm, EditNamedSetForm


# Named set views

@login_required
@never_cache
def named_set_new(request):
    """Create a new named set and redirect to named set settings"""

    if request.method == 'POST':
        form = NewNamedSetForm(request.POST)
        if 'name' in form.data:
            try:
                # If already exists, load the set
                named_set = NamedSet.objects.get(
                    name=slugify(form.data['name']))
                named_set.last_loaded = dt.datetime.now()
                named_set.save()
                return HttpResponseRedirect(named_set.get_absolute_url())
            except NamedSet.DoesNotExist:
                # Else, create the set
                if form.is_valid():
                    named_set = form.save()
                    return HttpResponseRedirect(reverse('namedset-edit',
                        kwargs={'namedset': named_set.name}))
    else:
        form = NewNamedSetForm()

    return render(request, 'sets/new.html', {
        'active': {'sets': True},
        'form': form,
        'recent_sets': request.session.get('recent_sets', None),
    })

@login_required
@never_cache
def named_set_edit(request, namedset):
    """Edit what comics is part of a named set"""

    named_set = get_object_or_404(NamedSet, name=namedset)

    if request.method == 'POST':
        form = EditNamedSetForm(request.POST, instance=named_set)
        if form.is_valid():
            form.save()
            # Update comic's number_of_set count
            for comic in Comic.objects.all():
                comic.number_of_sets = comic.namedset_set.count()
                comic.save()
            return HttpResponseRedirect(named_set.get_absolute_url())
    else:
        form = EditNamedSetForm(instance=named_set)

    kwargs = {
        'form': form,
        'set': named_set,
    }
    return render(request, 'sets/edit.html', kwargs)

@login_required
@never_cache
def named_set_show(request, namedset, year=None, month=None, day=None, days=1):
    """Show comics in this named set from one or more dates"""

    year = year and int(year)
    month = month and int(month)
    day = day and int(day)
    days = days and int(days)
    if not (1 <= days <= settings.COMICS_MAX_DAYS_IN_PAGE):
        raise Http404

    named_set = get_object_or_404(NamedSet, name=namedset)
    queryset = named_set.comics.all()
    page = get_navigation(request, 'namedset', instance=named_set,
        year=year, month=month, day=day, days=days)
    return generic_show(request, queryset, page,
        extra_context={'set': named_set})

@login_required
@never_cache
def named_set_latest(request, namedset):
    """Show latest releases from named set"""

    named_set = get_object_or_404(NamedSet, name=namedset)
    queryset = named_set.comics.all()
    page = get_navigation(request, 'namedset', instance=named_set, days=1,
        latest=True)
    return generic_show(request, queryset, page, latest=True,
        extra_context={'set': named_set})

@login_required
def named_set_year(request, namedset, year=None):
    """Redirect to first day of year if not in the future"""

    if int(year) > dt.date.today().year:
        raise Http404
    else:
        return HttpResponseRedirect(reverse('namedset-date', kwargs={
            'namedset': namedset,
            'year': year,
            'month': 1,
            'day': 1,
        }))


# User set views

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

    if int(year) > dt.date.today().year:
        raise Http404
    else:
        return HttpResponseRedirect(reverse('userset-date', kwargs={
            'year': year,
            'month': 1,
            'day': 1,
        }))
