import datetime as dt

from django.test import TestCase

from comics.common.models import Comic, Strip
from comics.common.utils import comic_strips as cs

class ComicStripsTestCase(TestCase):
    fixtures = ['test_strips.json']

    def setUp(self):
        self.comics = Comic.objects.all()
        self.strips = Strip.objects.all()
        self.num_comics = len(self.comics)
        self.num_strips = len(self.strips)

    def test_get_latest_strips(self):
        result = cs.get_latest_strips(self.comics)

        self.assertEquals(3, len(result))
        self.assertEquals('sinfest', result[0].comic.slug)
        self.assertEquals('userfriendly', result[1].comic.slug)
        self.assertEquals('xkcd', result[2].comic.slug)
        self.assertEquals(dt.date(2006, 5, 29), result[0].pub_date)
        self.assertEquals(dt.date(2006, 6, 1), result[1].pub_date)
        self.assertEquals(dt.date(2006, 6, 1), result[2].pub_date)

    def test_get_strips_from_interval(self):
        start_date = dt.date(2006, 5, 29)
        end_date = dt.date(2006, 5, 30)

        result = cs.get_strips_from_interval(self.comics, start_date, end_date)

        self.assertEquals(5, len(result))
        for strip in result:
            self.assertTrue(strip.pub_date >= start_date)
            self.assertTrue(strip.pub_date <= end_date)

    def test_add_strip_count(self):
        result = Strip.objects.all()
        num_strips = len(result)

        cs.add_strip_counter(result)

        self.assertTrue(len(result) > 0)
        self.assertEquals(num_strips, len(result))
        for i, item in enumerate(result):
            self.assertEquals(i, item.counter)

    def test_map_strips_to_comics(self):
        result = cs.map_strips_to_comics(self.comics, self.strips)

        self.assertTrue(len(result) > 0)
        self.assertEquals(self.num_comics, len(result))
        for comic, strips in result:
            if comic.slug in ('sinfest', 'userfriendly', 'xkcd'):
                self.assertTrue(len(strips) > 0)
            else:
                self.assertTrue(strips is None)

    def test_get_comic_strips_struct_latest(self):
        result = cs.get_comic_strips_struct(self.comics, latest=True)

        self.assertTrue(len(result) > 0)
        self.assertEquals(self.num_comics, len(result))
        # TODO Verify that get_latest_strips() is called

    def test_get_comic_strips_struct_interval(self):
        start_date = dt.date(2006, 5, 29)
        end_date = dt.date(2006, 5, 30)

        result = cs.get_comic_strips_struct(self.comics,
            start_date=start_date, end_date=end_date)

        self.assertTrue(len(result) > 0)
        self.assertEquals(self.num_comics, len(result))
        # TODO Verify that get_strips_from_interval() is called
