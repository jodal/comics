import datetime as dt

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.datastructures import SortedDict

from comics.core.models import Comic, Release
from comics.core.utils.comic_releases import get_comic_releases_struct
from comics.core.utils.navigation import get_navigation
from comics.aggregator.utils import get_comic_schedule

# Generic views

def generic_show(request, queryset, page, latest=False, extra_context=None):
    """Generic view for showing comics"""

    comics = get_comic_releases_struct(
        queryset,
        latest=latest,
        start_date=page.get('start_date', None),
        end_date=page.get('end_date', None))

    kwargs = {
        'active': {'home': True},
        'page': page,
        'comics': comics,
    }
    if extra_context is not None:
        kwargs.update(extra_context)
    return render(request, 'core/release-list.html', kwargs)


# One comic views

@login_required
def comic_list(request):
    """List all available comics"""

    return render(request, 'core/comic-list.html')

@login_required
def comic_show(request, comic, year=None, month=None, day=None, days=1):
    """Show one specific comic from one or more dates"""

    year = year and int(year)
    month = month and int(month)
    day = day and int(day)
    days = days and int(days)
    if not (1 <= days <= settings.COMICS_MAX_DAYS_IN_PAGE):
        raise Http404

    comic = get_object_or_404(Comic, slug=comic)
    queryset = [comic]
    page = get_navigation(request, 'comic', instance=comic,
        year=year, month=month, day=day, days=days)
    return generic_show(request, queryset, page)

@login_required
def comic_latest(request, comic):
    """Show latest release from comic"""

    comic = get_object_or_404(Comic, slug=comic)
    queryset = [comic]
    page = get_navigation(request, 'comic', instance=comic, days=1, latest=True)
    return generic_show(request, queryset, page, latest=True)

@login_required
def comic_year(request, comic, year):
    """Redirect to first day of year if not in the future"""

    if int(year) > dt.date.today().year:
        raise Http404
    else:
        return HttpResponseRedirect(reverse('comic-date', kwargs={
            'comic': comic,
            'year': year,
            'month': 1,
            'day': 1,
        }))


# Other views

def about(request):
    return render(request, 'core/about.html', {'active': {'about': True}})

@login_required
def status(request, days=21):
    timeline = SortedDict()
    first = dt.date.today() + dt.timedelta(days=1)
    last = dt.datetime.today() - dt.timedelta(days=days)

    releases = Release.objects.filter(pub_date__gte=last)
    releases = releases.select_related('comic__slug')
    releases = releases.order_by('comic__slug').distinct()

    for comic in Comic.objects.filter(active=True).order_by('slug'):
        schedule = get_comic_schedule(comic)
        timeline[comic] = []

        for i in range(days+2):
            day = first - dt.timedelta(days=i)
            classes = set()

            if not schedule:
                classes.add('unscheduled')
            elif int(day.strftime('%w')) in schedule:
                classes.add('scheduled')

            timeline[comic].append([classes, day, None])

    for release in releases:
        day = (first - release.pub_date).days
        timeline[release.comic][day][0].add('fetched')
        timeline[release.comic][day][2] = release

    days = [dt.date.today() - dt.timedelta(days=i) for i in range(-1, 22)]

    return render(request, 'core/status.html',
        {'days': days, 'timeline': timeline})

@login_required
def redirect(request, comic):
    comic = get_object_or_404(Comic, slug=comic)
    if comic.url is None:
        raise Http404
    return render(request, 'core/redirect.html', {'url': comic.url})

def robots(request):
    return HttpResponse('User-Agent: *\nDisallow: /\n', mimetype='text/plain')
