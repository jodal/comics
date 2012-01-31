import datetime as dt

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.views.decorators.cache import never_cache

from comics.core.models import Comic
from comics.core.utils.navigation import get_navigation
from comics.core.views import generic_show
from comics.sets.models import Set
from comics.sets.forms import NewSetForm, EditSetForm

@login_required
@never_cache
def named_set_new(request):
    """Create a new named set and redirect to named set settings"""

    if request.method == 'POST':
        form = NewSetForm(request.POST)
        if 'name' in form.data:
            try:
                # If already exists, load the set
                named_set = Set.objects.get(name=slugify(form.data['name']))
                named_set.last_loaded = dt.datetime.now()
                named_set.save()
                return HttpResponseRedirect(named_set.get_absolute_url())
            except Set.DoesNotExist:
                # Else, create the set
                if form.is_valid():
                    named_set = form.save()
                    return HttpResponseRedirect(reverse('namedset-edit',
                        kwargs={'namedset': named_set.name}))
    else:
        form = NewSetForm()

    kwargs = {
        'form': form,
        'recent_sets': request.session.get('recent_sets', None),
    }
    return render(request, 'sets/new.html', kwargs)

@login_required
@never_cache
def named_set_edit(request, namedset):
    """Edit what comics is part of a named set"""

    named_set = get_object_or_404(Set, name=namedset)

    if request.method == 'POST':
        form = EditSetForm(request.POST, instance=named_set)
        if form.is_valid():
            form.save()
            # Update comic's number_of_set count
            for comic in Comic.objects.all():
                comic.number_of_sets = comic.set_set.count()
                comic.save()
            return HttpResponseRedirect(named_set.get_absolute_url())
    else:
        form = EditSetForm(instance=named_set)

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

    named_set = get_object_or_404(Set, name=namedset)
    queryset = named_set.comics.all()
    page = get_navigation(request, 'namedset', instance=named_set,
        year=year, month=month, day=day, days=days)
    return generic_show(request, queryset, page,
        extra_context={'set': named_set})

@login_required
@never_cache
def named_set_latest(request, namedset):
    """Show latest releases from named set"""

    named_set = get_object_or_404(Set, name=namedset)
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
