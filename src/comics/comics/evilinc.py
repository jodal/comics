from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Evil Inc."
    language = "en"
    url = "http://evil-inc.com/"
    start_date = "2005-05-30"
    rights = "Brad J. Guigar - Colorist: Ed Ryzowski"


class Crawler(CrawlerBase):
    history_capable_date = "2005-05-30"
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        page_url = "http://evil-inc.com/%s/?post_type=comic" % (
            pub_date.strftime("%Y/%m/%d")
        )

        page = self.parse_page(page_url)

        url = page.src("img.attachment-large.wp-post-image")
        if not url:
            return
        url = url.replace("?fit=1024%2C1024", "")
        title = page.text(".post-title")
        return CrawlerImage(url, title)
