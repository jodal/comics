import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Yehuda Moon'
    language = 'en'
    url = 'http://www.yehudamoon.com/'
    start_date = '2008-01-22'
    rights = 'Rick Smith'

class Crawler(CrawlerBase):
    history_capable_date = '2008-01-22'
    time_zone = -5
    has_rerun_releases = False

    def crawl(self, pub_date):
        page_url = 'http://www.yehudamoon.com/index.php?date=%s' % \
            pub_date.strftime('%Y-%m-%d')
        page = self.parse_page(page_url)

        # It'll forward you to the most current day if it doesn't have
        # pub_date. Check *explicitly* to make sure this day exists and bug out
        # if not
        current_day = page.value('select[id=ss_select] option[value*=%s]' %
            pub_date.strftime('%Y-%m-%d'))

        if current_day is None:
            return

        url = page.src('div[id="ss_img_div"] img')
        # If we can't figure the title out, just don't store it
        try:
            title_full = page.text('option[value*="%s"]' %
                pub_date.strftime('%Y-%m-%d'))
            title = re.sub('^.*- *', '', title_full)
        except TypeError, e:
            title = None
        return CrawlerImage(url, title)
