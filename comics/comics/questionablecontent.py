from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Questionable Content"
    language = "en"
    url = "https://questionablecontent.net/"
    start_date = "2003-08-01"
    rights = "Jeph Jacques"


class Crawler(CrawlerBase):
    history_capable_days = 365
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "US/Eastern"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("https://www.questionablecontent.net/QCRSS.xml")
        for entry in feed.for_date(pub_date):
            title = entry.title
            url = entry.summary.src('img[src*="/comics/"]')
            text = entry.summary.text("p", allow_multiple=True)
            if len(text) > 1:
                text = text[1]
            else:
                text = None

            return CrawlerImage(url, title, text)
