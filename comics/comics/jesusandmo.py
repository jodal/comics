from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Jesus & Mo"
    language = "en"
    url = "http://www.jesusandmo.net/"
    start_date = "2005-11-24"
    rights = "Mohammed Jones, CC BY-NC-SA 3.0"


class Crawler(CrawlerBase):
    history_capable_date = "2005-11-24"
    schedule = "We"
    time_zone = "Europe/London"

    archive_page = None

    def crawl(self, pub_date):
        if not self.archive_page:
            page_url = "https://www.jesusandmo.net/archives/"
            self.archive_page = self.parse_page(page_url)

        release = self.archive_page.root.xpath(
            '//span[(@class="comic-archive-date") and '
            '(.="%s")]/../span[@class="comic-archive-title"]/a'
            % pub_date.strftime("%b %d, %Y")
        )
        if not release:
            return
        release = release[0]
        link = release.get("href")
        title = release.text
        release_page = self.parse_page(link)
        url = release_page.root.xpath('//div[@id="comic"]/img/@data-src')
        if not url:
            return
        url = url[0]
        text = release_page.root.xpath('//div[@class="entry"]/p')
        text = text[0].text if text else None

        return CrawlerImage(url, title, text)
