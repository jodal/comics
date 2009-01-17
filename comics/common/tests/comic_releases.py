import datetime as dt

from django.test import TestCase

from comics.common.models import Comic, Release
from comics.common.utils import comic_releases as cr

class ComicReleasesTestCase(TestCase):
    fixtures = ['test_releases.json']

    def setUp(self):
        self.comics = Comic.objects.all()
        self.releases = Release.objects.all()
        self.num_comics = len(self.comics)
        self.num_releases = len(self.releases)

    def test_get_latest_releases(self):
        result = cr.get_latest_releases(self.comics)

        self.assertEquals(3, len(result))
        self.assertEquals('sinfest', result[0].comic.slug)
        self.assertEquals('userfriendly', result[1].comic.slug)
        self.assertEquals('xkcd', result[2].comic.slug)
        self.assertEquals(dt.date(2006, 5, 29), result[0].pub_date)
        self.assertEquals(dt.date(2006, 6, 1), result[1].pub_date)
        self.assertEquals(dt.date(2006, 6, 1), result[2].pub_date)

    def test_get_releases_from_interval(self):
        start_date = dt.date(2006, 5, 29)
        end_date = dt.date(2006, 5, 30)

        result = cr.get_releases_from_interval(
            self.comics, start_date, end_date)

        self.assertEquals(5, len(result))
        for release in result:
            self.assertTrue(release.pub_date >= start_date)
            self.assertTrue(release.pub_date <= end_date)

    def test_add_release_count(self):
        result = Release.objects.all()
        num_releases = len(result)

        cr.add_release_counter(result)

        self.assertTrue(len(result) > 0)
        self.assertEquals(num_releases, len(result))
        for i, item in enumerate(result):
            self.assertEquals(i, item.counter)

    def test_map_releases_to_comics(self):
        result = cr.map_releases_to_comics(self.comics, self.releases)

        self.assertTrue(len(result) > 0)
        self.assertEquals(self.num_comics, len(result))
        for comic, releases in result:
            if comic.slug in ('sinfest', 'userfriendly', 'xkcd'):
                self.assertTrue(len(releases) > 0)
            else:
                self.assertEquals(0, len(releases))

    def test_get_comic_releases_struct_latest(self):
        result = cr.get_comic_releases_struct(self.comics, latest=True)

        self.assertTrue(len(result) > 0)
        self.assertEquals(self.num_comics, len(result))
        # TODO Verify that get_latest_releases() is called

    def test_get_comic_releases_struct_interval(self):
        start_date = dt.date(2006, 5, 29)
        end_date = dt.date(2006, 5, 30)

        result = cr.get_comic_releases_struct(self.comics,
            start_date=start_date, end_date=end_date)

        self.assertTrue(len(result) > 0)
        self.assertEquals(self.num_comics, len(result))
        # TODO Verify that get_releases_from_interval() is called
