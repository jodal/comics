import datetime
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import (
    DayArchiveView,
    ListView,
    MonthArchiveView,
    RedirectView,
    TemplateView,
    TodayArchiveView,
)

from comics.core.models import Comic, Release


@login_required
def comics_list(request):
    return render(request, 'browser/comics_list.html', {
        'active': {'comics_list': True},
        'my_comics': request.user.comics_profile.comics.all(),
    })


class LoginRequiredMixin(object):
    """Things common for views requiring the user to be logged in"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # This overide is here so that the login_required decorator can be
        # applied to all the views subclassing this class.
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

    def get_user(self):
        return self.request.user


class ComicMixin(object):
    """Things common for *all* views of comics"""

    @property
    def comic(self):
        if not hasattr(self, '_comic'):
            self._comic = get_object_or_404(
                Comic, slug=self.kwargs['comic_slug'])
        return self._comic

    def get_my_comics(self):
        return self.get_user().comics_profile.comics.all()


class ReleaseMixin(LoginRequiredMixin, ComicMixin):
    """Things common for *all* views of comic releases"""

    allow_future = True
    template_name = 'browser/release_list.html'

    def render_to_response(self, context, **kwargs):
        # We hook into render_to_response() instead of get_context_data()
        # because the date based views only populate the context with
        # date-related information right before render_to_response() is called.
        context.update(self.get_release_context_data(context))
        return super(ReleaseMixin, self).render_to_response(context, **kwargs)

    def get_release_context_data(self, context):
        # The methods called later in this method assumes that ``self.context``
        # contains what is already ready to be made available for the template.
        self.context = context

        return {
            'my_comics': self.get_my_comics(),

            'active': {'comics': True},
            'object_type': self.get_object_type(),
            'view_type': self.get_view_type(),

            'title': self.get_title(),
            'subtitle': self.get_subtitle(),

            'latest_url': self.get_latest_url(),
            'today_url': self.get_today_url(),
            'day_url': self.get_day_url(),
            'month_url': self.get_month_url(),
            'feed_url': self.get_feed_url(),
            'feed_title': self.get_feed_title(),

            'first_url': self.get_first_url(),
            'prev_url': self.get_prev_url(),
            'next_url': self.get_next_url(),
            'last_url': self.get_last_url(),
        }

    def get_object_type(self):
        return None

    def get_view_type(self):
        return None

    def get_title(self):
        return None

    def get_subtitle(self):
        return None

    def get_latest_url(self):
        return None

    def get_today_url(self):
        return None

    def get_day_url(self):
        return None

    def get_month_url(self):
        return None

    def get_feed_url(self):
        return None

    def get_feed_title(self):
        return None

    def get_first_url(self):
        return None

    def get_prev_url(self):
        return None

    def get_next_url(self):
        return None

    def get_last_url(self):
        return None


class ReleaseLatestView(ReleaseMixin, ListView):
    """Things common for all *latest* views"""

    def get_subtitle(self):
        return 'Latest releases'

    def get_view_type(self):
        return 'latest'


class ReleaseDateMixin(ReleaseMixin):
    """Things common for all *date based* views"""

    date_field = 'pub_date'
    month_format = '%m'


class ReleaseDayArchiveView(ReleaseDateMixin, DayArchiveView):
    """Things common for all *day* views"""

    def get_view_type(self):
        return 'day'

    def get_subtitle(self):
        return self.context['day'].strftime('%A %d %B %Y').replace(' 0', ' ')


class ReleaseTodayArchiveView(ReleaseDateMixin, TodayArchiveView):
    """Things common for all *today* views"""

    def get_view_type(self):
        return 'today'

    def get_subtitle(self):
        return 'Today'


class ReleaseMonthArchiveView(ReleaseDateMixin, MonthArchiveView):
    """Things common for all *month* views"""

    def get_view_type(self):
        return 'month'

    def get_subtitle(self):
        return self.context['month'].strftime('%B %Y')


class ReleaseFeedView(ComicMixin, ListView):
    """Things common for all *feed* views"""

    template_name = 'browser/release_feed.html'

    def get_context_data(self, **kwargs):
        context = super(ReleaseFeedView, self).get_context_data(**kwargs)
        context.update({
            'feed': {
                'title': self.get_feed_title(),
                'url': self.request.build_absolute_uri(self.get_feed_url()),
                'web_url': self.request.build_absolute_uri(self.get_web_url()),
                'base_url': self.request.build_absolute_uri('/'),
                'author': self.get_feed_author(),
                'updated': self.get_last_updated(),
            },
        })
        return context

    def render_to_response(self, context, **kwargs):
        return super(ReleaseFeedView, self).render_to_response(
            context, content_type='application/xml', **kwargs)

    def get_user(self):
        return get_object_or_404(
            User,
            comics_profile__secret_key=self.request.GET.get('key', None),
            is_active=True)

    def get_web_url(self):
        return self.get_latest_url()

    def get_feed_author(self):
        return settings.COMICS_SITE_TITLE

    def get_last_updated(self):
        try:
            return self.get_queryset().values_list('fetched', flat=True)[0]
        except IndexError:
            return timezone.now()


class MyComicsMixin(object):
    """Things common for all views of *my comics*"""

    def get_queryset(self):
        return Release.objects.select_related().filter(
            comic__in=self.get_my_comics()).order_by('pub_date')

    def get_object_type(self):
        return 'mycomics'

    def get_title(self):
        return 'My comics'

    def get_latest_url(self):
        return reverse('mycomics_latest')

    def get_today_url(self):
        return reverse('mycomics_today')

    def _get_last_pub_date(self):
        if not hasattr(self, '_last_pub_date'):
            self._last_pub_date = self.get_queryset().values_list(
                'pub_date', flat=True).order_by('-pub_date')[0]
        return self._last_pub_date

    def get_day_url(self):
        try:
            last_date = self._get_last_pub_date()
            return reverse('mycomics_day', kwargs={
                'year': last_date.year,
                'month': last_date.month,
                'day': last_date.day,
            })
        except IndexError:
            pass

    def get_month_url(self):
        try:
            last_month = self._get_last_pub_date()
            return reverse('mycomics_month', kwargs={
                'year': last_month.year,
                'month': last_month.month,
            })
        except IndexError:
            pass

    def get_feed_url(self):
        return '%s?key=%s' % (
            reverse('mycomics_feed'),
            self.get_user().comics_profile.secret_key)

    def get_feed_title(self):
        return 'My comics'


class MyComicsHome(LoginRequiredMixin, RedirectView):
    """Redirects the home page to my comics"""

    permanent = True

    def get_redirect_url(self, **kwargs):
        return reverse('mycomics_latest')


class MyComicsLatestView(MyComicsMixin, ReleaseLatestView):
    """View of the latest releases from my comics"""

    paginate_by = settings.COMICS_MAX_RELEASES_PER_PAGE

    def get_queryset(self):
        releases = super(MyComicsLatestView, self).get_queryset()
        return releases.order_by('-fetched')

    def get_first_url(self):
        page = self.context['page_obj']
        if page.number != page.paginator.num_pages:
            return reverse(
                'mycomics_latest_page_n',
                kwargs={'page': page.paginator.num_pages})

    def get_prev_url(self):
        page = self.context['page_obj']
        if page.has_next():
            return reverse(
                'mycomics_latest_page_n',
                kwargs={'page': page.next_page_number()})

    def get_next_url(self):
        page = self.context['page_obj']
        if page.has_previous():
            return reverse(
                'mycomics_latest_page_n',
                kwargs={'page': page.previous_page_number()})

    def get_last_url(self):
        page = self.context['page_obj']
        if page.number != 1:
            return reverse('mycomics_latest_page_n', kwargs={'page': 1})


class MyComicsNumReleasesSinceView(MyComicsLatestView):
    def get_num_releases_since(self):
        last_release_seen = get_object_or_404(
            Release, id=self.kwargs['release_id'])
        releases = super(MyComicsNumReleasesSinceView, self).get_queryset()
        return releases.filter(fetched__gt=last_release_seen.fetched).count()

    def render_to_response(self, context, **kwargs):
        data = json.dumps({
            'since_release_id': int(self.kwargs['release_id']),
            'num_releases': self.get_num_releases_since(),
            'seconds_to_next_check': settings.COMICS_BROWSER_REFRESH_INTERVAL,
        })
        return HttpResponse(data, content_type='application/json')


class MyComicsDayView(MyComicsMixin, ReleaseDayArchiveView):
    """View of releases from my comics for a given day"""

    def get_first_url(self):
        try:
            first_date = self.get_queryset().values_list(
                'pub_date', flat=True).order_by('pub_date')[0]
            if first_date < self.context['day']:
                return reverse('mycomics_day', kwargs={
                    'year': first_date.year,
                    'month': first_date.month,
                    'day': first_date.day,
                })
        except IndexError:
            pass

    def get_prev_url(self):
        prev_date = self.get_previous_day(self.context['day'])
        if prev_date:
            return reverse('mycomics_day', kwargs={
                'year': prev_date.year,
                'month': prev_date.month,
                'day': prev_date.day,
            })

    def get_next_url(self):
        next_date = self.get_next_day(self.context['day'])
        if next_date:
            return reverse('mycomics_day', kwargs={
                'year': next_date.year,
                'month': next_date.month,
                'day': next_date.day,
            })

    def get_last_url(self):
        try:
            last_date = self.get_queryset().values_list(
                'pub_date', flat=True).order_by('-pub_date')[0]
            if last_date > self.context['day']:
                return reverse('mycomics_day', kwargs={
                    'year': last_date.year,
                    'month': last_date.month,
                    'day': last_date.day,
                })
        except IndexError:
            pass


class MyComicsTodayView(MyComicsMixin, ReleaseTodayArchiveView):
    """View of releases from my comics for today"""

    allow_empty = True

    def get_prev_url(self):
        prev_date = self.get_previous_day(self.context['day'])
        if prev_date:
            return reverse('mycomics_day', kwargs={
                'year': prev_date.year,
                'month': prev_date.month,
                'day': prev_date.day,
            })


class MyComicsMonthView(MyComicsMixin, ReleaseMonthArchiveView):
    """View of releases from my comics for a given month"""

    def get_first_url(self):
        try:
            first_month = self.get_queryset().values_list(
                'pub_date', flat=True).order_by('pub_date')[0]
            if first_month < self.context['month']:
                return reverse('mycomics_month', kwargs={
                    'year': first_month.year,
                    'month': first_month.month,
                })
        except IndexError:
            pass

    def get_prev_url(self):
        prev_month = self.context['previous_month']
        if prev_month:
            return reverse('mycomics_month', kwargs={
                'year': prev_month.year,
                'month': prev_month.month,
            })

    def get_next_url(self):
        next_month = self.context['next_month']
        if next_month:
            return reverse('mycomics_month', kwargs={
                'year': next_month.year,
                'month': next_month.month,
            })

    def get_last_url(self):
        try:
            last_month = self.get_queryset().values_list(
                'pub_date', flat=True).order_by('-pub_date')[0]
            if last_month > self.context['month']:
                return reverse('mycomics_month', kwargs={
                    'year': last_month.year,
                    'month': last_month.month,
                })
        except IndexError:
            pass


class MyComicsYearView(LoginRequiredMixin, RedirectView):
    """Redirect anyone trying to view the full year to January"""

    permanent = True

    def get_redirect_url(self, **kwargs):
        return reverse('mycomics_month', kwargs={
            'year': kwargs['year'],
            'month': '1',
        })


class MyComicsFeed(MyComicsMixin, ReleaseFeedView):
    """Atom feed for releases from my comics"""

    def get_queryset(self):
        from_date = datetime.date.today() - datetime.timedelta(
            days=settings.COMICS_MAX_DAYS_IN_FEED)
        releases = super(MyComicsFeed, self).get_queryset()
        return releases.filter(fetched__gte=from_date).order_by('-fetched')


class OneComicMixin(object):
    """Things common for all views of a single comic"""

    def get_queryset(self):
        return (
            Release.objects.select_related()
            .filter(comic=self.comic)
            .order_by('pub_date'))

    def get_object_type(self):
        return 'onecomic'

    def get_title(self):
        return self.comic.name

    def get_latest_url(self):
        return reverse('comic_latest', kwargs={'comic_slug': self.comic.slug})

    def _get_recent_pub_dates(self):
        if not hasattr(self, '_recent_pub_dates'):
            self._recent_pub_dates = self.get_queryset().values_list(
                'pub_date', flat=True).order_by('-pub_date')[:2]
        return self._recent_pub_dates

    def get_today_url(self):
        if datetime.date.today() in self._get_recent_pub_dates():
            return reverse(
                'comic_today',
                kwargs={'comic_slug': self.comic.slug})

    def get_day_url(self):
        try:
            last_pub_date = self._get_recent_pub_dates()[0]
            return reverse('comic_day', kwargs={
                'comic_slug': self.comic.slug,
                'year': last_pub_date.year,
                'month': last_pub_date.month,
                'day': last_pub_date.day,
            })
        except IndexError:
            pass

    def get_month_url(self):
        try:
            last_pub_date = self._get_recent_pub_dates()[0]
            return reverse('comic_month', kwargs={
                'comic_slug': self.comic.slug,
                'year': last_pub_date.year,
                'month': last_pub_date.month,
            })
        except IndexError:
            pass

    def get_feed_url(self):
        return '%s?key=%s' % (
            reverse('comic_feed', kwargs={'comic_slug': self.comic.slug}),
            self.get_user().comics_profile.secret_key)

    def get_feed_title(self):
        return 'Comics from %s' % self.comic.name

    def get_first_url(self):
        try:
            first_date = self.get_queryset().values_list(
                'pub_date', flat=True).order_by('pub_date')[0]
            if first_date < self.get_current_day():
                return reverse('comic_day', kwargs={
                    'comic_slug': self.comic.slug,
                    'year': first_date.year,
                    'month': first_date.month,
                    'day': first_date.day,
                })
        except IndexError:
            pass

    def get_prev_url(self):
        prev_date = self.get_previous_day(self.get_current_day())
        if prev_date:
            return reverse('comic_day', kwargs={
                'comic_slug': self.comic.slug,
                'year': prev_date.year,
                'month': prev_date.month,
                'day': prev_date.day,
            })

    def get_next_url(self):
        next_date = self.get_next_day(self.get_current_day())
        if next_date:
            return reverse('comic_day', kwargs={
                'comic_slug': self.comic.slug,
                'year': next_date.year,
                'month': next_date.month,
                'day': next_date.day,
            })

    def get_last_url(self):
        try:
            last_pub_date = self._get_recent_pub_dates()[0]
            if last_pub_date > self.get_current_day():
                return reverse('comic_day', kwargs={
                    'comic_slug': self.comic.slug,
                    'year': last_pub_date.year,
                    'month': last_pub_date.month,
                    'day': last_pub_date.day,
                })
        except IndexError:
            pass


class OneComicLatestView(OneComicMixin, ReleaseLatestView):
    """View of the latest release from a single comic"""

    paginate_by = 1

    def get_queryset(self):
        releases = super(OneComicLatestView, self).get_queryset()
        return releases.order_by('-fetched')

    def get_current_day(self):
        try:
            return self._get_recent_pub_dates()[0]
        except IndexError:
            pass

    def get_previous_day(self, day):
        try:
            return self._get_recent_pub_dates()[1]
        except IndexError:
            pass

    def get_next_day(self, day):
        pass  # Nothing is newer than 'latest'


class OneComicDayView(OneComicMixin, ReleaseDayArchiveView):
    """View of the releases from a single comic for a given day"""

    def get_current_day(self):
        return self.context['day']


class OneComicTodayView(OneComicMixin, ReleaseTodayArchiveView):
    """View of the releases from a single comic for today"""

    def get_current_day(self):
        return self.context['day']


class OneComicMonthView(OneComicMixin, ReleaseMonthArchiveView):
    """View of the releases from a single comic for a given month"""

    def get_first_url(self):
        try:
            first_month = self.get_queryset().values_list(
                'pub_date', flat=True).order_by('pub_date')[0]
            if first_month < self.context['month']:
                return reverse('comic_month', kwargs={
                    'comic_slug': self.comic.slug,
                    'year': first_month.year,
                    'month': first_month.month,
                })
        except IndexError:
            pass

    def get_prev_url(self):
        prev_month = self.context['previous_month']
        if prev_month:
            return reverse('comic_month', kwargs={
                'comic_slug': self.comic.slug,
                'year': prev_month.year,
                'month': prev_month.month,
            })

    def get_next_url(self):
        next_month = self.context['next_month']
        if next_month:
            return reverse('comic_month', kwargs={
                'comic_slug': self.comic.slug,
                'year': next_month.year,
                'month': next_month.month,
            })

    def get_last_url(self):
        try:
            last_pub_date = self._get_recent_pub_dates()[0]
            if last_pub_date > self.context['month']:
                return reverse('comic_month', kwargs={
                    'comic_slug': self.comic.slug,
                    'year': last_pub_date.year,
                    'month': last_pub_date.month,
                })
        except IndexError:
            pass


class OneComicYearView(LoginRequiredMixin, RedirectView):
    """Redirect anyone trying to view the full year to January"""

    permanent = True

    def get_redirect_url(self, **kwargs):
        return reverse('comic_month', kwargs={
            'comic_slug': kwargs['comic_slug'],
            'year': kwargs['year'],
            'month': '1',
        })


class OneComicFeed(OneComicMixin, ReleaseFeedView):
    """Atom feed for releases of a single comic"""

    def get_queryset(self):
        from_date = datetime.date.today() - datetime.timedelta(
            days=settings.COMICS_MAX_DAYS_IN_FEED)
        releases = super(OneComicFeed, self).get_queryset()
        return releases.filter(fetched__gte=from_date).order_by('-fetched')


class OneComicWebsiteRedirect(LoginRequiredMixin, ComicMixin, TemplateView):
    template_name = 'browser/comic_website.html'

    def get_context_data(self, **kwargs):
        context = super(OneComicWebsiteRedirect, self).get_context_data(
            **kwargs)
        context['url'] = self.comic.url
        return context
