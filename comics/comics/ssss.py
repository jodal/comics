from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Stand Still. Stay Silent"
    language = "en"
    url = "http://www.sssscomic.com/"
    start_date = "2013-11-01"
    rights = "Minna Sundberg"


class Crawler(CrawlerBase):
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://sssscomic.com/ssss-feed.xml")
        for entry in feed.all():
            page = self.parse_page(entry.link)
            url = page.src("img.comicnormal")
            title = entry.title.replace("SSSS page", "Page")
            return CrawlerImage(url, title)
