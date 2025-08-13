import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "GU Comics"
    language = "en"
    url = "http://www.gucomics.com/"
    start_date = "2000-07-10"
    rights = "Woody Hearn"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = "2000-07-10"
    schedule = "Mo,We,Fr"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        page_url = "http://www.gucomics.com/%s" % pub_date.strftime("%Y%m%d")
        page = self.parse_page(page_url)

        title = page.texts("b")[0]
        title = title.replace('"', "")
        title = title.strip()

        text = page.texts(".main")[0]

        #  If there is a "---", the text after is not about the comic
        text = text[: text.find("---")]
        # If there is a "[ ", the text after is not part of the text
        text = text[: text.find("[ ")]
        text = text.strip()
        # Reduce any amount of newlines down to two newlines
        text = text.replace("\r", "")
        text = re.sub(r"\s*\n\n\s*", "\n\n", text)

        url = page.src('img[alt^="Comic for"]')
        return CrawlerImage(url, title, text)
