import datetime

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'VG Cats'
    language = 'en'
    url = 'http://www.vgcats.com/'
    start_date = '2001-09-09'
    rights = 'Scott Ramsoomair'

class Crawler(CrawlerBase):
    history_capable_date = '2001-09-09'
    time_zone = 'US/Eastern'

    # Without User-Agent set, the server returns empty responses
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        # FIXME: Seems like they are using gif images now and then
        if pub_date < datetime.date(2003, 5, 1):
            file_ext = 'gif'
        else:
            file_ext = 'jpg'
        url = 'http://www.vgcats.com/comics/images/%s.%s' % (
            pub_date.strftime('%y%m%d'), file_ext)
        return CrawlerImage(url)
