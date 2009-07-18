"""Utility functions for the view generic_show."""

from django.core.exceptions import ObjectDoesNotExist

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
    add_release_counter(releases)
    comics = map_releases_to_comics(comics, releases)
    return comics

def get_latest_releases(comics):
    """Returns the latest release for each comic"""

    releases = []
    for comic in comics:
        try:
            releases.append(
                comic.release_set.select_related(depth=1).latest())
        except ObjectDoesNotExist:
            continue
    return releases

def get_releases_from_interval(comics, start_date, end_date):
    """
    For each comic returns the releases published between start_date and
    end_date

    """

    releases = []
    for comic in comics:
        try:
            cr = comic.release_set.select_related(depth=1)
            if start_date == end_date:
                cr = cr.filter(pub_date=start_date)
            else:
                cr = cr.filter(pub_date__gte=start_date, pub_date__lte=end_date)
            cr = cr.order_by('pub_date')
            releases += cr
        except ObjectDoesNotExist:
            continue
    return releases

def add_release_counter(releases):
    """Add counter, which is used in navigation JavaScript, to releases"""

    for counter, release in enumerate(releases):
        release.counter = counter

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
