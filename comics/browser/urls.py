from django.conf.urls import url

from comics.browser import views

YEAR = r"(?P<year>(19|20)\d{2})"  # 1900-2099
MONTH = r"(?P<month>(0*[1-9]|1[0-2]))"  # 1-12
WEEK = r"week/(?P<week>(0*[1-9]|[1-4]\d|5[0-3]))"  # 1-53
DAY = r"(?P<day>(0*[1-9]|[1-2]\d|3[0-1]))"  # 1-31
DAYS = r"\+(?P<days>\d+)"
COMIC = r"(?P<comic_slug>[0-9a-z-_]+)"

urlpatterns = [
    url(r"^$", views.MyComicsHome.as_view(), name="home"),
    url(r"^all/$", views.comics_list, name="comics_list"),
    # Views of my comics selection
    url(r"^my/$", views.MyComicsLatestView.as_view(), name="mycomics_latest"),
    url(
        r"^my/page(?P<page>[0-9]+)/$",
        views.MyComicsLatestView.as_view(),
        name="mycomics_latest_page_n",
    ),
    url(
        fr"^my/{YEAR}/$",
        views.MyComicsYearView.as_view(),
        name="mycomics_year",
    ),
    url(
        fr"^my/{YEAR}/{MONTH}/$",
        views.MyComicsMonthView.as_view(),
        name="mycomics_month",
    ),
    url(
        fr"^my/{YEAR}/{MONTH}/{DAY}/$",
        views.MyComicsDayView.as_view(),
        name="mycomics_day",
    ),
    url(r"^my/today/$", views.MyComicsTodayView.as_view(), name="mycomics_today"),
    url(r"^my/feed/$", views.MyComicsFeed.as_view(), name="mycomics_feed"),
    url(
        r"^my/num-releases-since/(?P<release_id>\d+)/$",
        views.MyComicsNumReleasesSinceView.as_view(),
        name="mycomics_num_releases_since",
    ),
    # Views of a single comic
    url(
        fr"^{COMIC}/$",
        views.OneComicLatestView.as_view(),
        name="comic_latest",
    ),
    url(
        fr"^{COMIC}/{YEAR}/$",
        views.OneComicYearView.as_view(),
        name="comic_year",
    ),
    url(
        fr"^{COMIC}/{YEAR}/{MONTH}/$",
        views.OneComicMonthView.as_view(),
        name="comic_month",
    ),
    url(
        fr"^{COMIC}/{YEAR}/{MONTH}/{DAY}/$",
        views.OneComicDayView.as_view(),
        name="comic_day",
    ),
    url(
        fr"^{COMIC}/today/$",
        views.OneComicTodayView.as_view(),
        name="comic_today",
    ),
    url(
        fr"^{COMIC}/website/$",
        views.OneComicWebsiteRedirect.as_view(),
        name="comic_website",
    ),
    url(
        fr"^{COMIC}/feed/$",
        views.OneComicFeed.as_view(),
        name="comic_feed",
    ),
]
