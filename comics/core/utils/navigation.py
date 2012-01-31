"""Utils for building the time frame and navigation menus"""

import calendar
import datetime as dt
from urllib import unquote

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404

from comics.core.utils.time_frames import time_frames

def get_navigation(request, view_type, instance=None,
    year=None, month=None, day=None, days=7, latest=False):
    if year and month and not day and not latest:
        return navigation_month(request, view_type, instance=instance,
            year=year, month=month)
    else:
        return navigation_days(request, view_type, instance=instance,
            year=year, month=month, day=day, days=days, latest=latest)

def navigation_days(request, view_type, instance=None,
         year=None, month=None, day=None, days=7, latest=False):
    """
    Top comics
        navigation_days('top', year=2007, month=7, day=19)
    One comic
        navigation_days('comic', instance=comic, year=2007, month=7, day=19)
    Comic set
        navigation_days('namedset', instance=named_set, year=2007, month=7,
            day=19)
    """

    today = dt.date.today()
    one_day = dt.timedelta(1)

    # Start/end dates
    if days and not (year or month or day):
        start_date = today - one_day * (days - 1)
    else:
        try:
            start_date = dt.date(year, month, day)
        except ValueError:
            raise Http404
    end_date = start_date + one_day * (days - 1)
    if end_date > today:
        end_date = today

    # First/last dates
    first_date = None
    last_date = None
    if view_type == 'comic' and instance is not None:
        try:
            first_date = instance.release_set.order_by('pub_date'
                ).values('pub_date')[0]['pub_date']
            last_date = instance.release_set.values('pub_date'
                ).latest()['pub_date']
        except (IndexError, ObjectDoesNotExist):
            # The comic has no releases
            pass

    # Prev/next dates
    if view_type == 'comic' and instance is not None and days == 1:
        # When browsing a single comic, skip days without comics
        try:
            prev_date = instance.release_set.filter(pub_date__lt=start_date
                ).values('pub_date').latest()['pub_date']
        except ObjectDoesNotExist:
            # At first release
            prev_date = start_date
        try:
            next_date = instance.release_set.filter(pub_date__gt=start_date
                ).values('pub_date').order_by('pub_date')[0]['pub_date']
        except IndexError:
            # At latest release; next is in the future
            next_date = today + one_day
    else:
        # For all other views
        prev_date = start_date - one_day * days
        next_date = start_date + one_day * days

    # URLs
    if first_date is not None:
        first_kwargs = {
            'year': first_date.year,
            'month': first_date.month,
            'day': first_date.day,
        }
    if last_date is not None:
        last_kwargs = {
            'year': last_date.year,
            'month': last_date.month,
            'day': last_date.day,
        }
    prev_kwargs = {
        'year': prev_date.year,
        'month': prev_date.month,
        'day': prev_date.day,
    }
    next_kwargs = {
        'year': next_date.year,
        'month': next_date.month,
        'day': next_date.day,
    }
    if instance is not None:
        if first_date is not None:
            first_kwargs[view_type] = instance.slug
        if last_date is not None:
            last_kwargs[view_type] = instance.slug
        prev_kwargs[view_type] = instance.slug
        next_kwargs[view_type] = instance.slug
    if days > 1:
        view_name = '%s-date-days' % view_type
        if first_date is not None:
            first_kwargs['days'] = days
        if last_date is not None:
            last_kwargs['days'] = days
        prev_kwargs['days'] = days
        next_kwargs['days'] = days
    else:
        view_name = '%s-date' % view_type
    if first_date is None or start_date <= first_date <= end_date:
        first_url = None
    else:
        first_url = unquote(reverse(view_name, kwargs=first_kwargs))
    if last_date is None or start_date <= last_date <= end_date or latest:
        last_url = None
    else:
        last_url = unquote(reverse(view_name, kwargs=last_kwargs))
    if (prev_date == start_date
        or (first_date is not None and prev_date < first_date)):
        prev_date = None
        prev_url = None
    else:
        prev_url = unquote(reverse(view_name, kwargs=prev_kwargs))
    if (next_date > today
        or (last_date is not None and next_date > last_date)):
        next_date = None
        next_url = None
    else:
        next_url = unquote(reverse(view_name, kwargs=next_kwargs))

    # Title
    title = []
    if view_type == 'top':
        title.append('Top %d' % settings.COMICS_MAX_IN_TOP_LIST)
    elif view_type == 'comic':
        title.append(instance.name)
    elif view_type == 'namedset':
        title.append(instance.name)
    title.append('>')
    if latest:
        title.append('Latest')
    else:
        if start_date == end_date:
            title.append('%s' %
                start_date.strftime('%a %d %b %Y').replace(' 0', ' '))
        else:
            title.append('%s &ndash; %s' % (
                start_date.strftime('%a %d %b').replace(' 0', ' '),
                end_date.strftime('%a %d %b %Y').replace(' 0', ' ')
            ))
    title = ' '.join(title)

    if instance is not None:
        slug = instance.slug
    else:
        slug = None

    # Build struct
    return {
        'view_type': view_type,
        'title': title,
        'today': today,
        'time_frames': time_frames(view_type, start_date, slug,
            last_visit(request)),
        'start_date': start_date,
        'end_date': end_date,
        'first_date': first_date,   'first_url': first_url,
        'last_date': last_date,     'last_url': last_url,
        'prev_date': prev_date,      'prev_url': prev_url,
        'next_date': next_date,      'next_url': next_url,
    }

def navigation_month(request, view_type, instance=None, year=None, month=None):
    """
    Top comics
        navigation_month('top', year=2007, month=7)
    One comic
        navigation_month('comic', instance=comic, year=2007, month=7)
    Comic set
        navigation_month('namedset', instance=named_set, year=2007, month=7)
    """

    today = dt.date.today()
    one_day = dt.timedelta(1)

    if year is None:
        year = today.year
    if month is None:
        month = today.month

    # Start/end dates
    try:
        start_date = dt.date(year, month, 1)
        num_days = calendar.monthrange(year, month)[1]
        end_date = dt.date(year, month, num_days)
    except ValueError:
        raise Http404

    # First/last dates
    first_month = None
    last_month = None
    if view_type == 'comic' and instance is not None:
        try:
            first_release = instance.release_set.order_by('pub_date')[0]
            first_month = dt.date(first_release.pub_date.year,
                first_release.pub_date.month, 1)
            last_release = instance.release_set.latest()
            last_month_num_days = calendar.monthrange(
                last_release.pub_date.year,
                last_release.pub_date.month)[1]
            last_month = dt.date(last_release.pub_date.year,
                last_release.pub_date.month, last_month_num_days)
        except (IndexError, ObjectDoesNotExist):
            # Comic has no releases
            pass

    # Prev/next dates
    prev_month = (start_date - one_day)
    prev_num_days = calendar.monthrange(prev_month.year, prev_month.month)[1]
    prev_month = start_date - prev_num_days * one_day
    next_month = end_date + one_day

    # URLs
    if first_month is not None:
        first_kwargs = {
            'year': first_month.year,
            'month': first_month.month,
        }
    if last_month is not None:
        last_kwargs = {
            'year': last_month.year,
            'month': last_month.month,
        }
    prev_kwargs = {
        'year': prev_month.year,
        'month': prev_month.month,
    }
    next_kwargs = {
        'year': next_month.year,
        'month': next_month.month,
    }
    if instance is not None:
        if first_month is not None:
            first_kwargs[view_type] = instance.slug
        if last_month is not None:
            last_kwargs[view_type] = instance.slug
        prev_kwargs[view_type] = instance.slug
        next_kwargs[view_type] = instance.slug
    if first_month is None or first_month == start_date:
        first_url = None
    else:
        first_url = reverse('%s-month' % view_type, kwargs=first_kwargs)
    if last_month is None or last_month == end_date:
        last_url = None
    else:
        last_url = reverse('%s-month' % view_type, kwargs=last_kwargs)
    if first_month is not None and prev_month < first_month:
        prev_month = None
        prev_url = None
    else:
        prev_url = reverse('%s-month' % view_type, kwargs=prev_kwargs)
    if (next_month > today
        or (last_month is not None and next_month > last_month)):
        next_month = None
        next_url = None
    else:
        next_url = reverse('%s-month' % view_type, kwargs=next_kwargs)

    # Title
    title = []
    if view_type == 'top':
        title.append('Top %d' % settings.COMICS_MAX_IN_TOP_LIST)
    elif view_type == 'comic':
        title.append(instance.name)
    elif view_type == 'namedset':
        title.append(instance.name)
    title.append('>')
    title.append('%s' % start_date.strftime('%B %Y'))
    title = ' '.join(title)

    if instance is not None:
        slug = instance.slug
    else:
        slug = None

    # Build struct
    return {
        'view_type': view_type,
        'title': title,
        'today': today,
        'time_frames': time_frames(view_type, start_date, slug,
            last_visit(request)),
        'start_date': start_date,
        'end_date': end_date,
        'first_month': first_month, 'first_url': first_url,
        'last_month': last_month,   'last_url': last_url,
        'prev_month': prev_month,   'prev_url': prev_url,
        'next_month': next_month,   'next_url': next_url,
    }

def last_visit(request):
    if hasattr(request, 'session') and 'last_visit' in request.session:
        return request.session['last_visit']
    else:
        return dt.date.today()
