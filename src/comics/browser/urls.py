from django.urls import include, path, re_path

from comics.browser import views

YEAR = r"(?P<year>(19|20)\d{2})"  # 1900-2099
MONTH = r"(?P<month>(0*[1-9]|1[0-2]))"  # 1-12
DAY = r"(?P<day>(0*[1-9]|[1-2]\d|3[0-1]))"  # 1-31

urlpatterns = [
    path(
        "",
        views.MyComicsHome.as_view(),
        name="home",
    ),
    path(
        "all/",
        views.comics_list,
        name="comics_list",
    ),
    # Views of my comics selection
    path(
        "my/",
        include(
            [
                path(
                    "",
                    views.MyComicsLatestView.as_view(),
                    name="mycomics_latest",
                ),
                path(
                    "page<int:page>/",
                    views.MyComicsLatestView.as_view(),
                    name="mycomics_latest_page_n",
                ),
                re_path(
                    rf"^{YEAR}/$",
                    views.MyComicsYearView.as_view(),
                    name="mycomics_year",
                ),
                re_path(
                    rf"^{YEAR}/{MONTH}/$",
                    views.MyComicsMonthView.as_view(),
                    name="mycomics_month",
                ),
                re_path(
                    rf"^{YEAR}/{MONTH}/{DAY}/$",
                    views.MyComicsDayView.as_view(),
                    name="mycomics_day",
                ),
                path(
                    "today/",
                    views.MyComicsTodayView.as_view(),
                    name="mycomics_today",
                ),
                path(
                    "feed/",
                    views.MyComicsFeed.as_view(),
                    name="mycomics_feed",
                ),
                path(
                    "num-releases-since/<int:release_id>/",
                    views.MyComicsNumReleasesSinceView.as_view(),
                    name="mycomics_num_releases_since",
                ),
            ]
        ),
    ),
    # Views of a single comic
    path(
        "<slug:comic_slug>/",
        include(
            [
                path(
                    "",
                    views.OneComicLatestView.as_view(),
                    name="comic_latest",
                ),
                re_path(
                    rf"^{YEAR}/$",
                    views.OneComicYearView.as_view(),
                    name="comic_year",
                ),
                re_path(
                    rf"^{YEAR}/{MONTH}/$",
                    views.OneComicMonthView.as_view(),
                    name="comic_month",
                ),
                re_path(
                    rf"^{YEAR}/{MONTH}/{DAY}/$",
                    views.OneComicDayView.as_view(),
                    name="comic_day",
                ),
                path(
                    "today/",
                    views.OneComicTodayView.as_view(),
                    name="comic_today",
                ),
                path(
                    "website/",
                    views.OneComicWebsiteRedirect.as_view(),
                    name="comic_website",
                ),
                path(
                    "feed/",
                    views.OneComicFeed.as_view(),
                    name="comic_feed",
                ),
            ]
        ),
    ),
]
