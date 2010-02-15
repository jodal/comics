from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Questionable Content'
    language = 'en'
    url = 'http://questionablecontent.net/'
    start_date = '2003-08-01'
    rights = 'Jeph Jacques'

class Crawler(CrawlerBase):
    history_capable_date = '2003-08-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.questionablecontent.net/QCRSS.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            if url == None:
                continue
            title = entry.title

            # Construct the text as the "stuff under the image" on the page / feed.
            text = "\n\n".join( [x.strip() for x in entry.html(entry.description).text( 'p', allowmultiple=True ) if len(x.strip()) > 0] )

            return CrawlerImage(url, title=title, text=text)
