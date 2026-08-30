import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Nerf NOW!!"
    language = "en"
    url = "https://www.nerfnow.com/"
    start_date = "2009-09-02"
    rights = "Josué Pereira"


class Crawler(CrawlerBase):
    history_length_days = 14
    schedule = "Tu,We,Th,Fr,Sa"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("https://www.nerfnow.com/index.xml")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/img/"]')
            if url is None:
                continue
            url = url.replace("/large", ".png")
            title = entry.title

            # The feed holds the text as escaped markup, so read the page
            page = self.parse_page(entry.link)
            # Put together text from multiple paragraphs
            text = "\n\n".join(page.texts(".comment p")).strip()

            return CrawlerImage(url, title, text)
        return None
