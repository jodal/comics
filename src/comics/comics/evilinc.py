from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Evil Inc."
    language = "en"
    url = "https://www.evil-inc.com/"
    start_date = "2005-05-30"
    rights = "Brad J. Guigar - Colorist: Ed Ryzowski"


class Crawler(CrawlerBase):
    history_capable_days = 35
    schedule = "Tu,Th"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://www.evil-inc.com/comic/feed/")
        for entry in feed.for_date(pub_date):
            title = entry.title
            page = self.parse_page(entry.link)
            img = page.root.xpath('//div[@id="unspliced-comic"]/picture/img')
            if img is None:
                continue
            url = img[0].attrib["src"]
            return CrawlerImage(url, title)
