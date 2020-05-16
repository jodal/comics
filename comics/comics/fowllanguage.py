from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Fowl Language"
    language = "en"
    url = "http://www.fowllanguagecomics.com/"
    start_date = "2013-07-22"
    rights = "Brian Gordon"


class Crawler(CrawlerBase):
    history_capable_date = "2013-07-22"
    time_zone = "US/Eastern"
    headers = {"User-Agent": "Mozilla/5.0"}

    def crawl(self, pub_date):
        page_url = "https://www.fowllanguagecomics.com/archive"
        archive_page = self.parse_page(page_url)
        release = archive_page.root.xpath(
            '//p[(@class="ar-extra-text") and (.="%s")]/..'
            % pub_date.strftime("%b %d, %Y")
        )
        if not release:
            return
        release = release[0]
        title = release.xpath('p[@class="ar-text"]')
        title = title[0].text

        url = release.xpath("img/@data-lazy-src")
        url = url[0].replace("?fit=200%2C250&ssl=1", "")

        link = release.xpath('a[@class="ar-btn"]/@href')
        link = link[0]

        release_page = self.parse_page(link)
        bonus_link = release_page.root.xpath('//a[@class="bonus-btn"]/@href')
        if bonus_link:
            bonus_link = bonus_link[0]
            bonus_page = self.parse_page(bonus_link)
            bonus_url = bonus_page.root.xpath("//img/@data-lazy-src")
            bonus_url = bonus_url[0].replace("?fit=800%2C510&#038;ssl=1", "")
            bonus_title = bonus_page.root.xpath('//h2[@class="post-title"]')
            bonus_title = bonus_title[0].text
            return [
                CrawlerImage(url=url, title=title),
                CrawlerImage(url=bonus_url, title=bonus_title),
            ]
        else:
            return CrawlerImage(url=url, title=title)
