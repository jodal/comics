from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Hark, A Vagrant!'
    language = 'en'
    url = 'http://www.harkavagrant.com/'
    start_date = '2008-05-01'
    rights = 'Kate Beaton'


class Crawler(CrawlerBase):
    history_capable_days = 120
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.rsspect.com/rss/vagrant.xml')
        for entry in feed.for_date(pub_date):
            title = entry.title.replace('Hark, a Vagrant: ', '')
            urls = entry.summary.src('img', allow_multiple=True)
            for url in urls:
                if '/history/' in url or '/nonsense/' in url:
                    return CrawlerImage(url, title)
