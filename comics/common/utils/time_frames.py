"""Utils for building the time frame menus"""

import datetime as dt
from urllib import unquote

from django.core.urlresolvers import reverse

def time_frames(view_type, start_date, slug, last_visit):
    """Returns a list of time frame menu items"""

    result = generic_time_frames(view_type, slug, start_date)
    if view_type == 'set':
        result += set_time_frames(slug, last_visit)
    return result

def generic_time_frames(view_type, slug, start_date):
    """Returns a list of generic time frame menu items"""

    return [
        latest_time_frame(view_type, slug),
        a_day_time_frame(view_type, slug, start_date),
        a_week_time_frame(view_type, slug, start_date),
        this_month_time_frame(view_type, slug, start_date),
    ]

def set_time_frames(slug, last_visit):
    """Returns a list of time frame menu items specific for set views"""

    time_frame = new_since_last_visit_time_frame(slug, last_visit)
    if time_frame is not None:
        return [time_frame]
    else:
        return []

def latest_time_frame(view_type, slug):
    """Returns menu item for the "latest" time frame"""

    view_name = '%s-latest' % view_type
    kwargs = {}
    if slug:
        kwargs[view_type] = slug
    return {
        'title': 'Latest',
        'url': unquote(reverse(view_name, kwargs=kwargs)),
        'icon': 'lightning',
    }

def a_day_time_frame(view_type, slug, start_date):
    """Returns menu item for the "a day" time frame"""

    view_name = '%s-%s-days' % (view_type, last_or_date(start_date, 1))
    kwargs = {'days': 1}
    if slug:
        kwargs[view_type] = slug
    if not time_frame_ends_in_future(start_date, 1):
        kwargs['year'] = start_date.year
        kwargs['month'] = start_date.month
        kwargs['day'] = start_date.day
    return {
        'title': 'A day',
        'url': unquote(reverse(view_name, kwargs=kwargs)),
        'icon': 'calendar_view_day',
    }

def a_week_time_frame(view_type, slug, start_date):
    """Returns menu item for the "a week" time frame"""

    view_name = '%s-%s-days' % (view_type, last_or_date(start_date, 7))
    kwargs = {'days': 7}
    if slug:
        kwargs[view_type] = slug
    if not time_frame_ends_in_future(start_date, 7):
        kwargs['year'] = start_date.year
        kwargs['month'] = start_date.month
        kwargs['day'] = start_date.day
    return {
        'title': 'A week',
        'url': unquote(reverse(view_name, kwargs=kwargs)),
        'icon': 'calendar_view_week',
    }

def this_month_time_frame(view_type, slug, start_date):
    """Returns menu item for the "this month" time frame"""

    view_name = '%s-month' % view_type
    kwargs = {
        'year': start_date.year,
        'month': start_date.month,
    }
    if slug:
        kwargs[view_type] = slug
    return {
        'title': 'This month',
        'url': unquote(reverse(view_name, kwargs=kwargs)),
        'icon': 'calendar_view_month',
    }

def new_since_last_visit_time_frame(set_slug, last_visit):
    """
    Returns time frame called "new since last visit", given a set slug and a
    date for the user's last visit.

    """

    view_name = 'set-last-days'
    if last_visit == today():
        return None
    else:
        days_since_last_visit = (today() - last_visit).days
        kwargs = {'set': set_slug, 'days': days_since_last_visit}
        return {
            'title': 'New since last visit',
            'url': unquote(reverse(view_name, kwargs=kwargs)),
            'icon': 'user',
        }

def time_frame_ends_in_future(start_date, days):
    """Returns true if the time frame ends in the future"""

    return start_date + dt.timedelta(days) > today()

def last_or_date(start_date, days):
    """If time frame ends in the future, return 'last', else 'date'"""

    if time_frame_ends_in_future(start_date, days):
        return 'last'
    else:
        return 'date'

# For testability
today = dt.date.today
