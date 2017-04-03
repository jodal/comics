import datetime
from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render

from comics.aggregator.utils import get_comic_schedule
from comics.core.models import Comic, Release


@login_required
def status(request, num_days=21):
    today = datetime.date.today()
    timeline = OrderedDict()
    last = today - datetime.timedelta(days=num_days)

    releases = Release.objects.filter(pub_date__gte=last, comic__active=True)
    releases = releases.select_related().order_by('comic__slug').distinct()

    comics = Comic.objects.filter(active=True)
    comics = comics.annotate(last_pub_date=Max('release__pub_date'))
    comics = comics.order_by('last_pub_date')

    for comic in comics:
        if comic.last_pub_date:
            comic.days_since_last_release = (today - comic.last_pub_date).days
        else:
            comic.days_since_last_release = 1000

        schedule = get_comic_schedule(comic)
        timeline[comic] = []

        for i in range(num_days + 1):
            day = today - datetime.timedelta(days=i)
            classes = set()

            if not schedule:
                classes.add('unscheduled')
            elif int(day.strftime('%w')) in schedule:
                classes.add('scheduled')

            timeline[comic].append([classes, day, None])

    for release in releases:
        day = (today - release.pub_date).days
        timeline[release.comic][day][0].add('fetched')
        timeline[release.comic][day][2] = release

    days = [
        today - datetime.timedelta(days=i)
        for i in range(num_days + 1)]

    return render(request, 'status/status.html', {
        'active': {'status': True},
        'days': days,
        'timeline': timeline,
    })
