import datetime

from django.utils import unittest

from comics.core.utils import time_frames as tf

class TimeFramesTestCase(unittest.TestCase):
    def setUp(self):
        tf.today = lambda: datetime.date(2008, 2, 29)

    def test_time_frame_ends_in_future(self):
        start_date = datetime.date(2008, 2, 28)

        self.assertFalse(tf.time_frame_ends_in_future(start_date, 0))
        self.assertFalse(tf.time_frame_ends_in_future(start_date, 1))
        self.assertTrue(tf.time_frame_ends_in_future(start_date, 2))
        self.assertTrue(tf.time_frame_ends_in_future(start_date, 3))

    def test_last_or_date(self):
        start_date = datetime.date(2008, 2, 28)

        self.assertEquals('date', tf.last_or_date(start_date, 0))
        self.assertEquals('date', tf.last_or_date(start_date, 1))
        self.assertEquals('last', tf.last_or_date(start_date, 2))
        self.assertEquals('last', tf.last_or_date(start_date, 3))

    def test_new_since_last_visit_time_frame_when_last_visit_today(self):
        last_visit = datetime.date(2008, 2, 29)

        result = tf.new_since_last_visit_time_frame('a_set_slug', last_visit)

        self.assert_(result is None)

    def test_new_since_last_visit_time_frame_when_last_visit_yesterday(self):
        last_visit = datetime.date(2008, 2, 28)

        result = tf.new_since_last_visit_time_frame('a_set_slug', last_visit)

        self.assert_('title' in result)
        self.assert_('url' in result)
        self.assert_('icon' in result)

    def test_set_time_frames_when_last_visit_today(self):
        last_visit = datetime.date(2008, 2, 29)

        result = tf.set_time_frames('a_set_slug', last_visit)

        self.assertEquals(0, len(result))

    def test_set_time_frames_when_last_visit_yesterday(self):
        last_visit = datetime.date(2008, 2, 28)

        result = tf.set_time_frames('a_set_slug', last_visit)

        self.assertEquals(1, len(result))

    def test_generic_time_frames(self):
        view_type = 'comic'
        slug = 'a_comic_slug'
        start_date = datetime.date(2008, 2, 9)

        result = tf.generic_time_frames(view_type, slug, start_date)

        self.assert_(len(result) > 0)
        for item in result:
            self.assert_('title' in item)
            self.assert_('url' in item)
            self.assert_('icon' in item)

    def test_time_frames(self):
        start_date = datetime.date(2008, 2, 21)
        last_visit = datetime.date(2008, 2, 28)

        comic_result = tf.time_frames(
            'comic', start_date, 'a_comic_slug', last_visit)
        set_result = tf.time_frames(
            'namedset', start_date, 'a_set_slug', last_visit)

        self.assert_(len(comic_result) < len(set_result))
