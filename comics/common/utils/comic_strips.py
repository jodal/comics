"""Utility functions for the view generic_show."""

from django.core.exceptions import ObjectDoesNotExist

def get_comic_strips_struct(comics, latest=False,
                            start_date=None, end_date=None):
    """
    Takes a queryset of comics and returns a data structure ready for
    the templates to use

    """

    assert latest or (start_date is not None and end_date is not None)
    if latest:
        strips = get_latest_strips(comics)
    else:
        strips = get_strips_from_interval(comics,
            start_date, end_date)
    add_strip_counter(strips)
    comics = map_strips_to_comics(comics, strips)
    return comics

def get_latest_strips(comics):
    """Returns the latest strip for each comic"""

    strips = []
    for comic in comics:
        try:
            strips.append(
                comic.strip_set.select_related().latest())
        except ObjectDoesNotExist:
            continue
    return strips

def get_strips_from_interval(comics, start_date, end_date):
    """
    For each comic returns the strips published between start_date and
    end_date

    """

    strips = []
    for comic in comics:
        try:
            strips += comic.strip_set.select_related().filter(
                    pub_date__gte=start_date, pub_date__lte=end_date
                ).order_by('pub_date', 'fetched')
        except ObjectDoesNotExist:
            continue
    return strips

def add_strip_counter(strips):
    """Add counter, which is used in navigation JavaScript, to strips"""

    for counter, strip in enumerate(strips):
        strip.counter = counter

def map_strips_to_comics(comics, strips):
    """
    Returns a list of two-tuples where the first part is a comic and the second
    part all strips belonging to that comic

    """

    mapping = {}
    for strip in strips:
        if not strip.comic.slug in mapping:
            mapping[strip.comic.slug] = [strip]
        else:
            mapping[strip.comic.slug].append(strip)
    result = []
    for comic in comics:
        result.append((comic, mapping.get(comic.slug, None)))
    return result
