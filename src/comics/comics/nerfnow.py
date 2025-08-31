from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Nerf NOW!!"
    language = "en"
    url = "https://www.nerfnow.com/"
    start_date = "2009-09-02"
    rights = "Josué Pereira"


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = "Tu,We,Th,Fr,Sa"
    time_zone = "America/New_York"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("https://feeds.feedburner.com/nerfnow/full")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/img/"]')
            if url is None:
                continue
            url = url.replace("/large.jpg", ".png")
            title = entry.title

            # Put together text from multiple paragraphs
            text = "\n\n".join(entry.content0.texts("p")).strip()

            return CrawlerImage(url, title, text)
