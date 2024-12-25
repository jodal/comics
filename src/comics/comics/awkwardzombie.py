from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Awkward Zombie"
    language = "en"
    url = "http://www.awkwardzombie.com/"
    start_date = "2006-09-20"
    rights = "Katie Tiedrich"


class Crawler(CrawlerBase):
    history_capable_date = "2006-09-19"
    schedule = "Mo"
    time_zone = "US/Eastern"
    archive_page = None

    def crawl(self, pub_date):
        if not self.archive_page:
            page_url = "https://www.awkwardzombie.com/awkward-zombie/archive/"
            self.archive_page = self.parse_page(page_url)

        release = self.archive_page.root.xpath(
            "//div[(@class='archive-date') and contains(.,'%s')]/.."
            % pub_date.strftime("%m-%d-%y")
        )
        if not release:
            return
        release = release[0]
        title = release.xpath("div[@class='archive-title']/a")
        title = title[0]
        game = release.xpath("div[@class='archive-game']/a")
        game = game[0].text

        link = title.get("href")
        title = title.text
        release_page = self.parse_page(link)

        imgs = release_page.root.xpath("//img[@id='cc-comic']")
        if not imgs:
            return
        url = imgs[0].get("src")

        return CrawlerImage(url, title, game)
