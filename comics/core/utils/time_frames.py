"""Utils for building the time frame menus"""

import datetime
from urllib import unquote

from django.core.urlresolvers import reverse

def time_frames(view_type, slug, start_date):
    """Returns a list of time frame menu items"""

    return [
        latest_time_frame(view_type, slug),
        a_day_time_frame(view_type, slug, start_date),
        a_week_time_frame(view_type, slug, start_date),
        this_month_time_frame(view_type, slug, start_date),
    ]

def latest_time_frame(view_type, slug):
    """Returns menu item for the "latest" time frame"""

    view_name = '%s-latest' % view_type
    kwargs = {}
    if slug:
        kwargs[view_type] = slug
    return {
        'title': 'Latest',
        'url': unquote(reverse(view_name, kwargs=kwargs)),
        'icon': 'star',
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
        'title': 'Day',
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
        'title': 'Week',
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
        'title': 'Month',
        'url': unquote(reverse(view_name, kwargs=kwargs)),
        'icon': 'calendar_view_month',
    }

def time_frame_ends_in_future(start_date, days):
    """Returns true if the time frame ends in the future"""

    return start_date + datetime.timedelta(days) > today()

def last_or_date(start_date, days):
    """If time frame ends in the future, return 'last', else 'date'"""

    if time_frame_ends_in_future(start_date, days):
        return 'last'
    else:
        return 'date'

# For testability
today = datetime.date.today
