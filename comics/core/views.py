import datetime as dt

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

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
        'page': page,
        'comics': comics,
    }
    if extra_context is not None:
        kwargs.update(extra_context)
    return render_to_response('core/release-list.html', kwargs,
        context_instance=RequestContext(request))


### Top comics ###

def top_show(request, year=None, month=None, day=None, days=1):
    """Show top comics from one or more dates"""

    year = year and int(year)
    month = month and int(month)
    day = day and int(day)
    days = days and int(days)
    if not (1 <= days <= settings.COMICS_MAX_DAYS_IN_PAGE):
        raise Http404

    queryset = Comic.objects.all().order_by(
        '-number_of_sets', 'name')[:settings.COMICS_MAX_IN_TOP_LIST]
    page = get_navigation(request, 'top',
        year=year, month=month, day=day, days=days)
    return generic_show(request, queryset, page)

def top_latest(request):
    """Show latest release for each comic"""

    queryset = Comic.objects.all().order_by(
        '-number_of_sets', 'name')[:settings.COMICS_MAX_IN_TOP_LIST]
    page = get_navigation(request, 'top', days=1, latest=True)
    return generic_show(request, queryset, page, latest=True)

def top_year(request, year):
    """Redirect to first day of year if not in the future"""

    if int(year) > dt.date.today().year:
        raise Http404
    else:
        return HttpResponseRedirect(reverse('top-date', kwargs={
            'year': year,
            'month': 1,
            'day': 1,
        }))


### One comic ###

def comic_list(request):
    """List all available comics"""

    return render_to_response('core/comic-list.html',
        context_instance=RequestContext(request))

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

def comic_latest(request, comic):
    """Show latest release from comic"""

    comic = get_object_or_404(Comic, slug=comic)
    queryset = [comic]
    page = get_navigation(request, 'comic', instance=comic, days=1, latest=True)
    return generic_show(request, queryset, page, latest=True)

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


### Other views ###

def about(request):
    return render_to_response('core/about.html',
        context_instance=RequestContext(request))

def status(request, days=21):
    timeline = {}
    first = dt.date.today() + dt.timedelta(days=1)
    last = dt.datetime.today() - dt.timedelta(days=days)

    schedule_days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    releases = Release.objects.filter(pub_date__gte=last)
    releases = releases.select_related('comic__name')
    releases = releases.order_by('comic__name').distinct()

    for release in releases:
        if release.comic not in timeline:
            schedule = get_comic_schedule(release.comic)
            timeline[release.comic] = []

            for i in range(days+2):
                day = first - dt.timedelta(days=i)
                classes = set()
                
                if not schedule:
                    classes.add('unscheduled')
                elif int(day.strftime('%w')) in schedule:
                    classes.add('scheduled')

                timeline[release.comic].append([classes, day, None])

        day = (first - release.pub_date).days
        timeline[release.comic][day][0].add('fetched')
        timeline[release.comic][day][2] = release
        
    return render_to_response('core/status.html',
        {'timeline': timeline},
        context_instance=RequestContext(request))

def redirect(request, comic):
    comic = get_object_or_404(Comic, slug=comic)
    if comic.url is None:
        raise Http404
    return render_to_response('core/redirect.html', {'url': comic.url},
        context_instance=RequestContext(request))

def robots(request):
    return HttpResponse('User-Agent: *\nDisallow: /\n', mimetype='text/plain')

def widgets(request):
    return render_to_response('core/widgets.html',
        context_instance=RequestContext(request))
