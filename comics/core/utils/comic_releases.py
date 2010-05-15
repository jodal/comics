"""Utility functions for the view generic_show."""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from comics.core.models import Image, Release

def get_comic_releases_struct(comics, latest=False,
                            start_date=None, end_date=None):
    """
    Takes a queryset of comics and returns a data structure ready for
    the templates to use

    """

    assert latest or (start_date is not None and end_date is not None)
    if latest:
        releases = get_latest_releases(comics)
    else:
        releases = get_releases_from_interval(comics,
            start_date, end_date)
    releases = releases.order_by('pub_date')
    add_images(releases)
    comics = map_releases_to_comics(comics, releases)
    return comics

def get_latest_releases(comics):
    """Returns the latest release for each comic"""

    release_ids = Release.objects.values('comic_id')
    release_ids = release_ids.annotate(Max('id'))
    release_ids = release_ids.values_list('id__max', flat=True)
    return Release.objects.filter(id__in=release_ids).select_related('comic')

def get_releases_from_interval(comics, start_date, end_date):
    """
    For each comic returns the releases published between start_date and
    end_date

    """

    releases = Release.objects.filter(comic__in=comics).select_related('comic')
    if start_date == end_date:
        releases = releases.filter(pub_date=start_date)
    else:
        releases = releases.filter(pub_date__gte=start_date, pub_date__lte=end_date)
    return releases

def add_images(releases):
    """
    Get all images for release set instead of being stuck with one query
    per release.
    """
    images = Image.objects.filter(releases__in=releases).order_by('id')
    images = images.extra(select={'release_id': 'release_id'})
    mapping = {}
    for image in images:
        if image.release_id in mapping:
            mapping[image.release_id].append(image)
        else:
            mapping[image.release_id] = [image]

    for release in releases:
        release.set_ordered_images(mapping.get(release.id, []))

def map_releases_to_comics(comics, releases):
    """
    Returns a list of two-tuples where the first part is a comic and the second
    part all releases belonging to that comic

    """

    mapping = {}
    for release in releases:
        if not release.comic.slug in mapping:
            mapping[release.comic.slug] = [release]
        else:
            mapping[release.comic.slug].append(release)
    result = []
    for comic in comics:
        result.append((comic, mapping.get(comic.slug, [])))
    return result
