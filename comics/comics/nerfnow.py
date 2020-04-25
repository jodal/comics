# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Nerf NOW!!"
    language = "en"
    url = "http://www.nerfnow.com/"
    start_date = "2009-09-02"
    rights = "Josué Pereira"


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = "Tu,We,Th,Fr,Sa"
    time_zone = "US/Eastern"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/nerfnow/full")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/img/"]')
            if url is None:
                continue
            url = url.replace("/large.jpg", ".png")
            title = entry.title

            # Put together text from multiple paragraphs
            text_paragraphs = entry.content0.text("p", allow_multiple=True)
            if text_paragraphs is not None:
                text = "\n\n".join(text_paragraphs)
            else:
                text = None

            return CrawlerImage(url, title, text)
