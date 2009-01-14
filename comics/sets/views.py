import datetime as dt

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.template.defaultfilters import slugify
from django.views.decorators.cache import never_cache

from comics.common.models import Comic
from comics.common.utils.navigation import get_navigation
from comics.common.views import generic_show
from comics.sets.models import Set
from comics.sets.forms import NewSetForm, EditSetForm

@never_cache
def set_new(request):
    """Create a new set and redirect to set settings"""

    if request.method == 'POST':
        form = NewSetForm(request.POST)
        if 'name' in form.data:
            try:
                # If already exists, load the set
                comics_set = Set.objects.get(name=slugify(form.data['name']))
                comics_set.last_loaded = dt.datetime.now()
                comics_set.save()
                return HttpResponseRedirect(comics_set.get_absolute_url())
            except Set.DoesNotExist:
                # Else, create the set
                if form.is_valid():
                    comics_set = form.save()
                    return HttpResponseRedirect(reverse('set-edit',
                        kwargs={'set': comics_set.name}))
    else:
        form = NewSetForm()

    kwargs = {
        'form': form,
        'recent_sets': request.session.get('recent_sets', None),
    }
    return render_to_response('sets/new.html', kwargs,
        context_instance=RequestContext(request))

@never_cache
def set_edit(request, set):
    """Edit what comics is part of a set"""

    set = get_object_or_404(Set, name=set)

    if request.method == 'POST':
        form = EditSetForm(request.POST, instance=set)
        if form.is_valid():
            form.save()
            # Update comic's number_of_set count
            for comic in Comic.objects.all():
                comic.number_of_sets = comic.set_set.count()
                comic.save()
            return HttpResponseRedirect(set.get_absolute_url())
    else:
        form = EditSetForm(instance=set)

    kwargs = {
        'form': form,
        'set': set,
    }
    return render_to_response('sets/edit.html', kwargs,
        context_instance=RequestContext(request))

@never_cache
def set_show(request, set, year=None, month=None, day=None, days=1):
    """Show comics in this set from one or more dates"""

    year = year and int(year)
    month = month and int(month)
    day = day and int(day)
    days = days and int(days)
    if not (1 <= days <= settings.COMICS_MAX_DAYS_IN_PAGE):
        raise Http404

    set = get_object_or_404(Set, name=set)
    queryset = set.comics.all()
    page = get_navigation(request, 'set', instance=set,
        year=year, month=month, day=day, days=days)
    return generic_show(request, queryset, page, extra_context={'set': set})

@never_cache
def set_latest(request, set):
    """Show latest strips from set"""

    set = get_object_or_404(Set, name=set)
    queryset = set.comics.all()
    page = get_navigation(request, 'set', instance=set, days=1, latest=True)
    return generic_show(request, queryset, page, latest=True,
        extra_context={'set': set})

def set_year(request, set, year=None):
    """Redirect to first day of year if not in the future"""

    if int(year) > dt.date.today().year:
        raise Http404
    else:
        return HttpResponseRedirect(reverse('set-date', kwargs={
            'set': set,
            'year': year,
            'month': 1,
            'day': 1,
        }))
