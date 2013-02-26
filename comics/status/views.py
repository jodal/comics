import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.datastructures import SortedDict

from comics.core.models import Comic, Release
from comics.aggregator.utils import get_comic_schedule


@login_required
def status(request, days=21):
    timeline = SortedDict()
    first = datetime.date.today() + datetime.timedelta(days=1)
    last = datetime.date.today() - datetime.timedelta(days=days)

    releases = Release.objects.filter(pub_date__gte=last, comic__active=True)
    releases = releases.select_related().order_by('comic__slug').distinct()

    for comic in Comic.objects.filter(active=True).order_by('slug'):
        schedule = get_comic_schedule(comic)
        timeline[comic] = []

        for i in range(days + 2):
            day = first - datetime.timedelta(days=i)
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

    days = [datetime.date.today() - datetime.timedelta(days=i)
        for i in range(-1, 22)]

    return render(request, 'status/status.html', {
        'days': days,
        'timeline': timeline,
    })
