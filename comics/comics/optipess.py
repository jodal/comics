from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Optipess"
    language = "en"
    url = "http://www.optipess.com/"
    start_date = "2008-12-01"
    rights = "Kristian Nygård"


class Crawler(CrawlerBase):
    history_capable_date = "2008-12-01"
    schedule = "Mo,Fr"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        # Find the post for the requested date
        archive_page = self.parse_page(
            "https://www.optipess.com/archive/?archive_year=%s"
            % pub_date.strftime("%Y")
        )
        date_string = pub_date.strftime("%b %-d")

        post_link = archive_page.root.xpath(
            '//td[(@class="archive-date") and '
            '(.="%s")]/../td[@class="archive-title"]/a' % date_string
        )

        if not post_link:
            return
        else:
            post_link = post_link[0]

        title = post_link.text
        # Fetch the actual post
        page = self.parse_page(post_link.get("href"))
        img = page.root.xpath('//div[@id="comic"]/img')
        if not img:
            img = page.root.xpath('//div[@id="comic"]/a/img')

        url = img[0].get("src")
        text = img[0].get("title")

        return CrawlerImage(url, title, text)
