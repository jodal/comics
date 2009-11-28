from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'The Perry Bible Fellowship'
    language = 'en'
    url = 'http://www.pbfcomics.com/'
    start_date = '2001-01-01'
    history_capable_days = 1
    time_zone = -5
    rights = 'Nicholas Gurewitch'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        pass # XXX Comic no longer published
